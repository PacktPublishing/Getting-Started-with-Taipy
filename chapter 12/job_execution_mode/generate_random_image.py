import time

import numpy as np
import plotly.express as px
import taipy as tp
from PIL import Image
from taipy import Config, Gui
from taipy.core import Status
from taipy.core.config import Config
from taipy.core.notification import (
    CoreEventConsumerBase,
    EventEntityType,
    EventOperation,
    Notifier,
)
from taipy.gui import builder as tgb
from taipy.gui import notify


def notify_color_matrix(state, id_name):
    color = id_name.split("_")[1]  # example id_name: "create_blue_matrix"
    if color == "image":
        notify(state, "s", f"Created Image!")
        image_matrix = scenario_image.image_node.read()
        state.image = create_imshow_fig_rgb(image_matrix)

    else:  # reg, green, blue
        notify(state, "i", f"Created {color} matrix!")


class SpecificCoreConsumer(CoreEventConsumerBase):
    def __init__(self, gui):
        self.gui = gui
        reg_id, queue = Notifier.register(entity_type=EventEntityType.JOB)
        super().__init__(reg_id, queue)

    def process_event(self, event):
        if (
            event.operation == EventOperation.UPDATE
            and event.entity_type == EventEntityType.JOB
            and event.attribute_value == Status.COMPLETED
        ):
            print(event)
            id_name = event.metadata.get("task_config_id")
            self.gui.broadcast_callback(notify_color_matrix, [id_name])


def generate_random_matrix(rows, cols):
    """
    Generates a matrix of random integers between 0 and 255.

    Args:
        rows: Number of rows in the matrix.
        cols: Number of columns in the matrix.

    Returns:
        A numpy array representing the matrix.
    """
    print("generating channel...")
    time.sleep(5)
    return np.random.randint(0, 256, size=(rows, cols), dtype=np.uint8)


def create_image_from_matrix(
    red_matrix, green_matrix, blue_matrix, filename="./random_image.png"
):
    """
    Creates an image from three matrices representing RGB channels.

    Args:
        red_matrix: Numpy array for the red channel.
        green_matrix: Numpy array for the green channel.
        blue_matrix: Numpy array for the blue channel.
        filename: The name of the output image file (e.g., "rgb_image.png").
    Returns:
        Numpy array with rgb data.
    """

    print("generating image...")
    rgb_image = np.stack([red_matrix, green_matrix, blue_matrix], axis=2)
    img = Image.fromarray(rgb_image)
    img.save(filename)

    return rgb_image


def create_imshow_fig_rgb(rgb_image):
    fig = px.imshow(rgb_image)
    return fig


def generate_image(state):
    # state.scenario_image.submit(wait=True)
    state.scenario_image.submit()
    image_matrix = scenario_image.image_node.read()

    state.image = create_imshow_fig_rgb(image_matrix)


image = None

with tgb.Page() as image_page:
    tgb.text("# Generate a random image!", mode="md")
    tgb.button(label="Generate!", on_action=generate_image)
    tgb.chart(figure="{image}")

if __name__ == "__main__":

    # Uncomment to run in parallel!
    Config.configure_job_executions(mode="standalone", max_nb_of_workers=3)

    # Data Nodes
    rows_node_config = Config.configure_data_node("rows_node", default_data=600)
    columns_node_config = Config.configure_data_node("columns_node", default_data=400)

    red_matrix_node_config = Config.configure_data_node("red_matrix_node")
    green_matrix_node_config = Config.configure_data_node("green_matrix_node")
    blue_matrix_node_config = Config.configure_data_node("blue_matrix_node")

    image_node_config = Config.configure_data_node("image_node", default_data=1)

    # Tasks
    create_red_matrix_task = Config.configure_task(
        id="create_red_matrix",
        function=generate_random_matrix,
        input=[rows_node_config, columns_node_config],
        output=red_matrix_node_config,
    )
    create_green_matrix_task = Config.configure_task(
        id="create_green_matrix",
        function=generate_random_matrix,
        input=[rows_node_config, columns_node_config],
        output=green_matrix_node_config,
    )
    create_blue_matrix_task = Config.configure_task(
        id="create_blue_matrix",
        function=generate_random_matrix,
        input=[rows_node_config, columns_node_config],
        output=blue_matrix_node_config,
    )

    create_image = Config.configure_task(
        id="create_image_matrix",
        function=create_image_from_matrix,
        input=[
            red_matrix_node_config,
            green_matrix_node_config,
            blue_matrix_node_config,
        ],
        output=image_node_config,
    )

    # Configuration
    image_scenario_config = Config.configure_scenario(
        id="my_scenario",
        task_configs=[
            create_red_matrix_task,
            create_green_matrix_task,
            create_blue_matrix_task,
            create_image,
        ],
    )
    Config.export("config_image.toml")

    tp.Orchestrator().run()

    scenario_image = tp.create_scenario(image_scenario_config)

    gui = Gui(page=image_page)
    SpecificCoreConsumer(gui).start()
    gui.run(
        # use_reloader=True,
    )
