from typing import Tuple

class DIIEngine:
    """
    DII = (Salary - (Rent * 1.15)) / Rent
    Rent * 1.15 accounts for approx. 15% additional expenses (ABL, utilities).
    """
    
    @staticmethod
    def calculate_dii(salary: float, rent: float) -> float:
        if rent <= 0:
            return 0.0
        # Formula: (Salary - 1.15 * Rent) / Rent
        return (salary - (rent * 1.15)) / rent

    def get_dii_for_city(self, rent: float, salary_tiers: Tuple[float, float, float, float, float]) -> dict:
        # salary_tiers ahora incluye: (min, median, prof, mean, moda)
        min_s, med_s, prof_s, mean_s, moda_s = salary_tiers

        def calc_net_diff(salary):
            return salary - (rent * 1.15)

        return {
            "min": self.calculate_dii(min_s, rent),
            "median": self.calculate_dii(med_s, rent),
            "professional": self.calculate_dii(prof_s, rent),
            "mean": self.calculate_dii(mean_s, rent),
            "mode": self.calculate_dii(moda_s, rent),
            "net_diff_median": calc_net_diff(med_s),
            "net_diff_mean": calc_net_diff(mean_s),
            "net_diff_mode": calc_net_diff(moda_s),
        }
