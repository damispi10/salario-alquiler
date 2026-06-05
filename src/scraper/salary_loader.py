import pandas as pd
from src.db.manager import DBManager

class SalaryLoader:
    def __init__(self, db: DBManager):
        self.db = db

    def load_indec_data(self, csv_path: str = None):
        """
        Imports INDEC regional salary data.
        If csv_path is None, use a mock baseline for MVP.
        """
        if csv_path:
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                self.db.save_salary(row['region'], row['min'], row['median'], row['prof'])
        else:
            # MVP Mock Data for Conurbano Bonaerense
            mock_data = [
                ("La Matanza", 320000, 520000, 850000),
                ("Quilmes", 310000, 500000, 800000),
                ("Lomas de Zamora", 310000, 500000, 800000),
                ("San Fernando", 300000, 480000, 780000),
                ("Tigre", 330000, 550000, 900000),
                ("Moreno", 280000, 420000, 700000),
                ("Tres de Febrero", 310000, 510000, 820000),
            ]
            for region, min_s, med_s, prof_s in mock_data:
                self.db.save_salary(region, min_s, med_s, prof_s)
