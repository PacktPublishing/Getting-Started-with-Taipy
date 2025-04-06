import os

import geopandas as gpd
import pandas as pd
import rasterio
from algorithms.algorithms import get_ndvi, get_polygon, get_time_series, reduce_by_time
from scipy.signal import savgol_filter
from taipy import Config, Scope


def read_gpkg(file, layer):
    """
    Reads a layer from a GeoPackage file and returns it as a GeoDataFrame.

    Args:
        file (str): Path to the GeoPackage (.gpkg) file
        layer (str): Name of the layer to read from the GeoPackage

    Returns:
        gpd.GeoDataFrame: The loaded geographic data with geometry column
    """
    gdf = gpd.read_file(filename=file, layer=layer)
    return gdf


def download_ndvi(ndvi, park_name, year):
    """
    Downloads an NDVI data cube as TIFF (if needed) and returns the image data.

    Args:
        ndvi: NDVI data cube to be downloaded (np Array)
        park_name (str): Name of the park/location to include in filename
        year (int/str): Year of the data to include in filename

    Returns:
        numpy.ndarray: 2D array containing the NDVI image data
    """
    image_name = f"./data/tif_images/{park_name} - {year}.tif"

    # Download if file doesn't exist
    if not os.path.exists(image_name):
        print(f"Downloading {image_name}...")
        ndvi.download(image_name)
        print("Download complete")

    # Load and return the TIFF data
    with rasterio.open(image_name) as src:
        return src.read(1)  # Return first band as numpy array


def download_time_series(ndvi_timeseries, park_name, year):
    """
    Downloads NDVI time series (if needed) and returns processed DataFrame.

    Args:
        ndvi_timeseries (openeo.DataCube): The time series data to download
        park_name (str): Name of the park/location for filename
        year (int): Year of the data for filename

    Returns:
        pd.DataFrame: Processed time series with:
                     - DateTime index
                     - 'ndvi' column
                     - Sorted chronologically
                     - Time-interpolated missing values
    """
    filename = f"./data/time_series/{park_name} - {year}.csv"

    # Download if needed
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        job = ndvi_timeseries.execute_batch(
            out_format="CSV", title=f"{park_name} - {year}"
        )
        job.get_results().download_file(
            filename
        )  # Raw file download,- different from Data Node's CSV
        print("Download complete")

    # Load and process
    df = pd.read_csv(filename, index_col=0)
    df.index = pd.to_datetime(df.index)
    df = df.rename(columns={"band_unnamed": "ndvi"})
    df = df.drop(columns="feature_index", errors="ignore")
    df.sort_index(inplace=True)
    df = df.interpolate(method="time")

    # Apply Savitzky-Golay Smoothing
    window_length = 5
    polyorder = 2
    df["ndvi"] = savgol_filter(df["ndvi"], window_length, polyorder)
    df["date"] = df.index

    return df


def read_tif(park_name, year):
    """
    Reads a NDVI TIFF file and returns the image data as a numpy array.

    Args:
        park_name (str): Name of the park/location used in the filename
        year (int or str): Year of the data used in the filename

    Returns:
        numpy.ndarray: 2D array containing NDVI values from the TIFF file
    """
    tif_image = f"{park_name} - {year}.tif"

    with rasterio.open(tif_image) as src:
        ndvi_image = src.read(1)  # NDVI is one band

    return ndvi_image


#################################
### Global Data Nodes         ###
#################################

gdf_paris_parks_node_config = Config.configure_generic_data_node(
    id="gdf_paris_parks",
    read_fct=read_gpkg,
    read_fct_args=["./data/paris_parks.gpkg", "parks_polygons"],
    scope=Scope.GLOBAL,
)
df_paris_parks_node_config = Config.configure_csv_data_node(
    id="df_paris_parks",
    default_path="./data/paris_parks.csv",
    scope=Scope.GLOBAL,
)
gdf_paris_parks_centroids_node_config = Config.configure_generic_data_node(
    id="gdf_paris_parks_centroids",
    read_fct=read_gpkg,
    read_fct_args=["./data/paris_parks.gpkg", "parks_centroids"],
    scope=Scope.GLOBAL,
)

#################################
### Selection Data Nodes      ###
#################################

selected_year_data_node_config = Config.configure_data_node(
    id="selected_year", default_data=2024
)
park_id_data_node_config = Config.configure_data_node(id="park_id")

park_name_data_node_config = Config.configure_data_node(id="park_name")

#################################
### Intermediate Data Nodes   ###
#################################

polygon_data_node_config = Config.configure_data_node(id="polygon")
ndvi_data_node_config = Config.configure_data_node(id="ndvi")
reduced_t_ndvi_data_node_config = Config.configure_data_node(id="reduced_t_ndvi")


#################################
### Output Data Nodes         ###
#################################
ndvi_tif_as_np_data_node_config = Config.configure_data_node(id="tif_image")
ndvi_time_series_data_node_config = Config.configure_data_node(
    id="datacube_time_series"
)

ndvi_time_series_tabular_data_node_config = Config.configure_csv_data_node(
    id="ndvi_time_series"
)

#################################
### Tasks                     ###
#################################
get_polygon_task_config = Config.configure_task(
    id="get_polygon",
    function=get_polygon,
    input=[gdf_paris_parks_node_config, park_id_data_node_config],
    output=polygon_data_node_config,
)

get_ndvi_task_config = Config.configure_task(
    id="get_ndvi",
    function=get_ndvi,
    input=[polygon_data_node_config, selected_year_data_node_config],
    output=ndvi_data_node_config,
)

reduce_by_time_task_config = Config.configure_task(
    id="reduce_by_time",
    function=reduce_by_time,
    input=ndvi_data_node_config,
    output=reduced_t_ndvi_data_node_config,
)

download_ndvi_task_config = Config.configure_task(
    id="download_ndvi",
    function=download_ndvi,
    input=[
        reduced_t_ndvi_data_node_config,
        park_name_data_node_config,
        selected_year_data_node_config,
    ],
    output=ndvi_tif_as_np_data_node_config,
)

get_time_series_task_config = Config.configure_task(
    id="get_time_series",
    function=get_time_series,
    input=[ndvi_data_node_config, polygon_data_node_config],
    output=ndvi_time_series_data_node_config,
)

download_time_series_task_config = Config.configure_task(
    id="download_time_series",
    function=download_time_series,
    input=[
        ndvi_time_series_data_node_config,
        park_name_data_node_config,
        selected_year_data_node_config,
    ],
    output=ndvi_time_series_tabular_data_node_config,
)


#################################
### Scenario                  ###
#################################

ndvi_scenario_config = Config.configure_scenario(
    id="ndvi_scenario",
    task_configs=[
        get_polygon_task_config,
        get_ndvi_task_config,
        reduce_by_time_task_config,
        download_ndvi_task_config,
        get_time_series_task_config,
        download_time_series_task_config,
    ],
)


Config.export("config.toml")
