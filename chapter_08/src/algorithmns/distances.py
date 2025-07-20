import numpy as np
import pandas as pd


def haversine_vectorized(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance (in km) between two points on Earth.
    """
    lat1 = np.radians(lat1[:, np.newaxis])  # shape (n, 1)
    lon1 = np.radians(lon1[:, np.newaxis])  # shape (n, 1)
    lat2 = np.radians(lat2[np.newaxis, :])  # shape (1, m)
    lon2 = np.radians(lon2[np.newaxis, :])  # shape (1, m)

    dlat = lat2 - lat1  # shape (n, m)
    dlon = lon2 - lon1  # shape (n, m)

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    R = 6371.0  # Radius of Earth in kilometers
    return R * c  # shape (n, m)


def calculate_distance_matrix(df_warehouses, df_customers):
    """
    Returns a DataFrame where rows = warehouses, columns = customers,
    and values = distances in km.
    """

    # Coordinates as np.arrays
    lat_wh = df_warehouses["latitude"].to_numpy()
    lon_wh = df_warehouses["longitude"].to_numpy()
    lat_cu = df_customers["latitude"].to_numpy()
    lon_cu = df_customers["longitude"].to_numpy()

    # Compute distance matrix using vectorized haversine
    distance_matrix = haversine_vectorized(lat_wh, lon_wh, lat_cu, lon_cu)

    return pd.DataFrame(
        distance_matrix, index=df_warehouses.index, columns=df_customers.index
    )
