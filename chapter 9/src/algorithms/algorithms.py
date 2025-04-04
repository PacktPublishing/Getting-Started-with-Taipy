import os

import openeo


def get_polygon(gdf_paris_parks, id):
    """
    Retrieves the geometry (polygon or multipolygon) of a specific park
    identified by its `id` from the given GeoDataFrame.

    Args:
        gdf_paris_parks (GeoDataFrame): A GeoDataFrame containing park geometries
        id (int): The identifier of the park to retrieve

    Returns:
        dict: The polygon
    """
    polygon = gdf_paris_parks[gdf_paris_parks["id"] == id].geometry.__geo_interface__
    return polygon


def connect_to_copernicus(
    client_id, client_secret, url="https://openeo.dataspace.copernicus.eu"
):
    """
    Establishes a connection to ESA's Copernicus Data Space using OpenEO.

    Args:
        client_id (str): The client ID for authentication
        client_secret (str): The client secret for authentication
        url (str, optional): The Copernicus OpenEO service URL. Defaults to the official ESA endpoint

    Returns:
        openeo.Connection: The authenticated connection object
    """
    connection = openeo.connect(url)
    connection.authenticate_oidc_client_credentials(
        client_id=client_id, client_secret=client_secret
    )
    return connection


def create_datacube(polygon, start, end, connection):
    """
    Creates a data cube for Sentinel-2 imagery over a given spatial and temporal extent.

    Args:
        polygon (dict): The spatial extent to get data about
        start (str): The start date of the time range (YYYY-MM-DD)
        end (str): The end date of the time range (YYYY-MM-DD)
        connection (openeo.Connection): The OpenEO connector

    Returns:
        openeo.DataCube: Data cube with the selected bands
    """
    datacube = connection.load_collection(
        "SENTINEL2_L2A",
        temporal_extent=[start, end],
        spatial_extent=polygon,
        bands=["B04", "B08", "SCL"],  # Red and NIR for NDVI and SCL for clouds
    )
    return datacube


def mask_clouds(datacube):
    """
    Applies a cloud mask to a given data cube by filtering out cloud-covered pixels.

    Args:
    datacube (openeo.DataCube): The data cube containing Sentinel-2 bands.

    Returns:
    openeo.DataCube: The masked data cube with clouds removed.
    """
    scl = datacube.band("SCL")
    cloud_mask = (scl == 8) | (scl == 9)  # Cloud classes
    datacube = datacube.mask(cloud_mask)
    return datacube


def create_ndvi(datacube):
    """
    Calculates Normalized Difference Vegetation Index (NDVI) from a given data cube.

    Args:
        datacube (openeo.DataCube): The data cube containing Red (B04)
            and Near Infra-Red (NIR - B08) bands.

    Returns:
        openeo.DataCube: The computed NDVI data cube
    """
    ndvi = (datacube.band("B08") - datacube.band("B04")) / (
        datacube.band("B08") + datacube.band("B04")
    )
    return ndvi


def get_ndvi(polygon, year):
    """
    Retrieves the NDVI data cube for a given park and year.

    Args:
    polygon (dict): The spatial extent of the park in geo-interface format.
    park_name (str): The name of the park (not used in processing but for reference).
    year (int or str): The year for which NDVI data is required.

    Returns:
    openeo.DataCube: The NDVI data cube for the given year and location.
    """
    connection = connect_to_copernicus(
        client_id=os.getenv("COPERNICUS_ID"),
        client_secret=os.getenv("COPERNICUS_SECRET"),
    )

    datacube = create_datacube(polygon, f"{year}-01-01", f"{year}-12-31", connection)
    datacube = mask_clouds(datacube)
    ndvi = create_ndvi(datacube)

    return ndvi


def reduce_by_time(ndvi):
    """
    Reduces the temporal dimension of an NDVI data cube by computing the median value.

    Args:
        ndvi (openeo.DataCube): The NDVI data cube with a temporal dimension

    Returns:
        openeo.DataCube: The time-reduced data cube with median values
    """
    ndvi_time_reduced = ndvi.reduce_dimension(dimension="t", reducer="median")
    return ndvi_time_reduced


def get_time_series(ndvi, polygon):
    """
    Computes a median NDVI time series for the specified polygon geometry.

    Args:
        ndvi (openeo.DataCube): The NDVI data cube with temporal dimension
        polygon (dict): GeoJSON-like polygon geometry for spatial aggregation

    Returns:
        openeo.DataCube: Time series data cube with median NDVI values
    """
    timeseries = ndvi.aggregate_spatial(geometries=polygon, reducer="median")
    return timeseries
