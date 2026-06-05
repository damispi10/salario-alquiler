import sqlite3
import os
from typing import List, Tuple, Any

class DBManager:
    def __init__(self, db_path: str = "vivienda.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with open("src/db/schema.sql", "r") as f:
            schema = f.read()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(schema)
            # Migración: agregar columnas nuevas si la tabla ya existe sin ellas
            migraciones = [
                "ALTER TABLE regional_salaries ADD COLUMN mean_salary REAL DEFAULT 0",
                "ALTER TABLE regional_salaries ADD COLUMN moda_salary REAL DEFAULT 0",
            ]
            for sql in migraciones:
                try:
                    conn.execute(sql)
                except sqlite3.OperationalError:
                    pass  # la columna ya existe, ignorar

    def save_rental(self, city: str, price: float, currency: str = "ARS", url: str = "seed"):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO rental_data (city, price, currency, source_url) VALUES (?, ?, ?, ?)",
                (city, price, currency, url)
            )

    def save_salary(self, region: str, min_s: float, med_s: float, prof_s: float, mean_s: float = 0, moda_s: float = 0):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO regional_salaries (region, min_salary, median_salary, prof_salary, mean_salary, moda_salary) VALUES (?, ?, ?, ?, ?, ?)",
                (region, min_s, med_s, prof_s, mean_s, moda_s)
            )

    def get_salaries(self, region: str) -> Tuple[float, float, float, float, float]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT min_salary, median_salary, prof_salary, mean_salary, moda_salary FROM regional_salaries WHERE region = ?", 
                (region,)
            )
            row = cursor.fetchone()
            return row if row else (0.0, 0.0, 0.0, 0.0, 0.0)

    def get_rental_stats(self, city: str) -> Tuple[float, int]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT AVG(price), COUNT(*) FROM rental_data WHERE city = ?", 
                (city,)
            )
            return cursor.fetchone()

    def get_last_scraped_at(self, city: str) -> Any:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT MAX(scraped_at) FROM rental_data WHERE city = ?", 
                (city,)
            )
            return cursor.fetchone()[0]
