import geopandas as gpd
from taipy import Config, Scope

from algorithms.algorithms import (
    download_ndvi,
    download_time_series,
    get_ndvi,
    get_polygon,
    get_time_series,
    reduce_by_time,
)


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
id_name_data_node_config = Config.configure_data_node(id="id_name")

#################################
### Intermediate Data Nodes   ###
#################################

polygon_data_node_config = Config.configure_data_node(id="polygon")
ndvi_data_node_config = Config.configure_data_node(id="ndvi")
reduced_t_ndvi_data_node_config = Config.configure_data_node(id="reduced_t_ndvi")


#################################
### Output Data Nodes         ###
#################################
ndvi_tiff_as_np_data_node_config = Config.configure_data_node(id="tiff_image")
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
    input=[gdf_paris_parks_node_config, id_name_data_node_config],
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
        id_name_data_node_config,
        selected_year_data_node_config,
    ],
    output=ndvi_tiff_as_np_data_node_config,
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
        id_name_data_node_config,
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
