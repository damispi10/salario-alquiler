#!/usr/bin/env python3
# seed_data.py — Carga datos actualizados del Conurbano Bonaerense en la DB
#
# Fuentes:
#   Alquileres: Zonaprop - Infobae (Mayo 2026)
#   Salarios:   INDEC / Observatorio del Conurbano (UNGS) - Abril 2026
#   SMVM:       $357.800 (Decreto abril 2026)

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.db.manager import DBManager

# Limpiar datos anteriores y forzar recreación del schema
import os
import sqlite3
db_path = "vivienda.db"
if os.path.exists(db_path):
    os.remove(db_path)
    print("🧹 Base de datos eliminada. Recreando schema...\n")

db = DBManager()

# ── Datos ACTUALIZADOS del Conurbano Bonaerense (mayo 2026) ──

# Salarios: (Minimo, Mediana, Profesional, Promedio, Moda)
#   - Minimo: SMVM oficial
#   - Moda: el sueldo que más gente cobra (base de la pirámide)
#   - Mediana: el sueldo del medio
#   - Promedio: media aritmética (tirado por los sueldos altos)
#   - Profesional: sueldo de trabajador calificado
salarios = {
    "La Matanza":      (357800, 750000, 1300000, 820000, 390000),
    "Quilmes":         (357800, 780000, 1350000, 860000, 400000),
    "Lomas de Zamora": (357800, 760000, 1320000, 840000, 395000),
    "San Fernando":    (357800, 800000, 1400000, 890000, 410000),
    "Tigre":           (357800, 850000, 1500000, 950000, 420000),
    "Moreno":          (357800, 700000, 1200000, 760000, 380000),
    "Tres de Febrero": (357800, 770000, 1350000, 850000, 400000),
}

# Alquiler promedio mensual (departamento 2 ambientes - 50m²)
# Basado en Zonaprop / Infobae - Mayo 2026
#   GBA Norte promedio: $778.265
#   GBA Oeste promedio: $616.231
#   GBA Sur  promedio:  $609.450
alquileres = {
    "La Matanza":      580000,
    "Quilmes":         610000,
    "Lomas de Zamora": 615000,
    "San Fernando":    700000,
    "Tigre":           810000,
    "Moreno":          500000,
    "Tres de Febrero": 620000,
}

# 1. Cargar salarios
print("📊 SALARIOS:")
for ciudad, (minimo, mediana, profesional, promedio, moda) in salarios.items():
    db.save_salary(ciudad, minimo, mediana, profesional, promedio, moda)
    print(f"  {ciudad:20s}  Mín: ${minimo:>7,}  |  Moda: ${moda:>7,}  |  Med: ${mediana:>7,}  |  Prom: ${promedio:>7,}  |  Prof: ${profesional:>7,}")

# 2. Cargar alquileres
print("\n🏠 ALQUILERES:")
for ciudad, precio in alquileres.items():
    db.save_rental(ciudad, precio)
    print(f"  {ciudad:20s}  ${precio:>9,} /mes")

print("\n🎯 ¡Datos ACTUALIZADOS del Conurbano cargados exitosamente!")
print("▶ Ejecutá: streamlit run src/ui/app.py")
