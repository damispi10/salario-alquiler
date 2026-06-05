import sys
from pathlib import Path

# Ensure src/ modules are importable when running directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.db.manager import DBManager
from src.engine.calculator import DIIEngine

st.set_page_config(page_title="Vivienda MVP - Índice DII", layout="wide")

db = DBManager()
engine = DIIEngine()

st.title("🏠 Índice DII Vivienda - Conurbano Bonaerense")
st.markdown("Evaluando el **Índice de Ingreso Disponible (DII)** según **Moda, Mediana y Promedio** salarial.")

# --- Recuperación de Datos ---
def get_data():
    regions = ["La Matanza", "Quilmes", "Lomas de Zamora", "San Fernando", "Tigre", "Moreno", "Tres de Febrero"]
    data = []
    for r in regions:
        rent_stats = db.get_rental_stats(r)
        rent = rent_stats[0] if rent_stats and rent_stats[0] else 0.0
        
        # Ahora devuelve 5 valores: (min, median, prof, mean, mode)
        salaries = db.get_salaries(r)
        dii_results = engine.get_dii_for_city(rent, salaries)
        
        data.append({
            "Localidad": r,
            "Alquiler": round(rent),
            # DII por medida estadística
            "DII_Moda": dii_results["mode"],
            "DII_Mediana": dii_results["median"],
            "DII_Promedio": dii_results["mean"],
            "DII_Profesional": dii_results["professional"],
            # Sueldos
            "Sueldo_Moda": round(salaries[4]),
            "Sueldo_Mediana": round(salaries[1]),
            "Sueldo_Promedio": round(salaries[3]),
            "Sueldo_Profesional": round(salaries[2]),
            # Diferencia neta
            "Diferencia_Moda": round(dii_results["net_diff_mode"]),
            "Diferencia_Mediana": round(dii_results["net_diff_median"]),
            "Diferencia_Promedio": round(dii_results["net_diff_mean"]),
        })
    return pd.DataFrame(data)

df = get_data()

# --- Selector de medida estadística ---
st.sidebar.header("📊 Medida Salarial")
medida = st.sidebar.radio(
    "Seleccioná la medida estadística para el análisis:",
    ["Moda (sueldo más frecuente)", "Mediana (sueldo del medio)", "Promedio (media)"]
)

col_dii_map = {
    "Moda (sueldo más frecuente)": "DII_Moda",
    "Mediana (sueldo del medio)": "DII_Mediana",
    "Promedio (media)": "DII_Promedio",
}
col_sueldo = {
    "Moda (sueldo más frecuente)": "Sueldo_Moda",
    "Mediana (sueldo del medio)": "Sueldo_Mediana",
    "Promedio (media)": "Sueldo_Promedio",
}
col_diff = {
    "Moda (sueldo más frecuente)": "Diferencia_Moda",
    "Mediana (sueldo del medio)": "Diferencia_Mediana",
    "Promedio (media)": "Diferencia_Promedio",
}

selected_dii = col_dii_map[medida]
selected_sueldo = col_sueldo[medida]
selected_diff = col_diff[medida]

# --- Visualización 1: Mapa ---
st.subheader(f"🗺️ Mapa de Asequibilidad - {medida}")
map_data = df.copy()
coords = {
    "La Matanza":      [-34.86, -58.50],
    "Quilmes":         [-34.85, -58.33],
    "Lomas de Zamora": [-34.82, -58.41],
    "San Fernando":    [-34.62, -58.67],
    "Tigre":           [-34.52, -58.84],
    "Moreno":          [-34.77, -58.83],
    "Tres de Febrero": [-34.73, -58.63],
}
map_data["lat"] = map_data["Localidad"].map(lambda x: coords[x][0])
map_data["lon"] = map_data["Localidad"].map(lambda x: coords[x][1])

fig_map = px.scatter_map(
    map_data, lat="lat", lon="lon", color=selected_dii,
    size=selected_sueldo, hover_name="Localidad",
    hover_data={"Alquiler": True, selected_sueldo: True, selected_dii: True, "lat": False, "lon": False},
    color_continuous_scale=px.colors.diverging.RdYlGn,
    zoom=9, map_style="carto-positron",
    title=f"DII según {medida}"
)
fig_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)

# --- Comparativa rápida ---
col1, col2, col3 = st.columns(3)
promedio_dii = df[selected_dii].mean()
mejor_ciudad = df.loc[df[selected_dii].idxmax(), "Localidad"]
peor_ciudad = df.loc[df[selected_dii].idxmin(), "Localidad"]

col1.metric("🏆 Mejor Ciudad", mejor_ciudad, f"DII: {df[selected_dii].max():.2f}")
col2.metric("📉 Peor Ciudad", peor_ciudad, f"DII: {df[selected_dii].min():.2f}")
col3.metric("📊 DII Promedio General", f"{promedio_dii:.2f}")

# --- Gráfico de Burbujas ---
st.subheader("🎯 Relación Alquiler vs. DII")
fig_bubble = px.scatter(
    df, x="Alquiler", y=selected_dii,
    size=selected_sueldo, color="Localidad",
    text="Localidad",
    labels={"Alquiler": "Alquiler Mensual (ARS)", selected_dii: f"DII ({medida})"},
    title=f"Costo del Alquiler vs. Asequibilidad — {medida}"
)
fig_bubble.update_traces(textposition='top center')
st.plotly_chart(fig_bubble, use_container_width=True)

# --- Tabla de Comparación Salarial ---
st.subheader("📋 Comparativa Salarial por Ciudad")
col_salarios = ["Localidad", "Sueldo_Moda", "Sueldo_Mediana", "Sueldo_Promedio", "Sueldo_Profesional"]
col_labels = {
    "Localidad": "Localidad", "Sueldo_Moda": "💰 Moda", "Sueldo_Mediana": "💰 Mediana",
    "Sueldo_Promedio": "💰 Promedio", "Sueldo_Profesional": "💰 Profesional"
}
df_salarios = df[col_salarios].copy()
for c in col_salarios[1:]:
    df_salarios[c] = df_salarios[c].apply(lambda x: f"${x:,.0f}")
df_salarios = df_salarios.rename(columns=col_labels)
st.dataframe(df_salarios, use_container_width=True)

# --- Ranking de Asequibilidad ---
st.subheader(f"🏅 Ranking de Asequibilidad — {medida}")
ranking_cols = ["Localidad", selected_sueldo, "Alquiler", selected_diff, selected_dii]
ranking_labels = {
    "Localidad": "Localidad",
    selected_sueldo: f"Sueldo ({medida})",
    "Alquiler": "Alquiler",
    selected_diff: "Diferencia Neta ($)",
    selected_dii: f"DII ({medida})"
}
df_ranking = df[ranking_cols].sort_values(by=selected_dii, ascending=False).copy()
for c in [selected_sueldo, "Alquiler", selected_diff]:
    df_ranking[c] = df_ranking[c].apply(lambda x: f"${x:,.0f}")
df_ranking[selected_dii] = df_ranking[selected_dii].apply(lambda x: f"{x:.2f}")
df_ranking = df_ranking.rename(columns=ranking_labels)
st.dataframe(df_ranking, use_container_width=True)

st.info(
    "📐 **Fórmula DII**: (Sueldo − (Alquiler × 1.15)) ÷ Alquiler  |  "
    "**Valores > 0** → el sueldo cubre el alquiler y servicios.  |  "
    "**Moda** = sueldo más frecuente | **Mediana** = valor central | **Promedio** = media aritmética"
)

# --- Fuentes de datos ---
st.markdown("---")
st.subheader("📚 Fuentes de Datos y Referencias")
st.markdown("""
| Dato | Fuente | Período |
|------|--------|---------|
| **Precios de alquiler** (2 ambientes, 50m²) | Zonaprop — Informe mensual vía Infobae | **Mayo 2026** |
| **Salario Mínimo Vital y Móvil (SMVM)** | Decreto del Poder Ejecutivo Nacional | **Abril 2026** — $357.800 |
| **Salario por deciles (Conurbano)** | Observatorio del Conurbano Bonaerense — UNGS | **Abril 2026** |
| **Índice de Salarios (general)** | INDEC — Índice de Salarios (IS) | **Febrero 2026** (último disponible) |
| **Canasta Básica Total (referencia)** | INDEC — CBT | **Abril 2026** — $1.434.464 |

> ⚠️ **Nota sobre los datos salariales:** Los valores de Moda, Mediana, Promedio y Profesional por localidad
> son estimaciones basadas en los deciles del Observatorio del Conurbano (UNGS) y el índice de salarios del INDEC.
> No existen estadísticas públicas con desagregación mensual por municipio del Conurbano. Si tenés datos más
> precisos, podés actualizar `seed_data.py` y recargar.
""")
