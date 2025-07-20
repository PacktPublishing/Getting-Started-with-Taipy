from dataclasses import dataclass

import pandas as pd


@dataclass
class ProblemData:
    df_warehouses: pd.DataFrame
    df_customers: pd.DataFrame
    distance_matrix: pd.DataFrame
    price_per_km: float = 4
    co2_per_km: float = 2
