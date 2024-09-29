import rasterio
import taipy as tp
from taipy import Config, Orchestrator, Scope


def read_raster_as_numpy_array(raster_path):
    """Reads a raster image and returns it as a NumPy array.

    Args:
        raster_path: The path to the raster image file.

    Returns:
        A NumPy array representing the raster data.
    """

    with rasterio.open(raster_path) as src:
        data = src.read()  # Reads all bands into a 3D NumPy array
        return data


tokyo_image_node_config = Config.configure_generic_data_node(
    id="tokyo_image",
    read_fct=read_raster_as_numpy_array,
    read_fct_args=["../data/tokyo_snow.jpg"],
    scope=Scope.GLOBAL,
)

orchestrator = Orchestrator()
orchestrator.run()


tokyo_image_data_node = tp.create_global_data_node(tokyo_image_node_config)

tokyo_image_raster = tokyo_image_data_node.read()

print(tokyo_image_raster)
