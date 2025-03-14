import numpy as np
import pandas as pd
from taipy.gui import Gui
from taipy.gui import builder as tgb


def create_linear_df(a, b, x_min, x_max, num_points=100):
    """
    Creates a pandas DataFrame representing the linear equation y = ax + b.

    Args:
      a: Slope of the line.
      b: Y-intercept of the line.
      x_min: Minimum value for the x-axis.
      x_max: Maximum value for the x-axis.
      num_points: Number of data points to generate.

    Returns:
      pandas.DataFrame: A DataFrame with 'x' and 'y' columns.
    """
    x_values = np.linspace(x_min, x_max, num_points)
    y_values = a * x_values + b
    return pd.DataFrame({"x": x_values, "y": y_values})


def go_to_page_3(state):
    with state as s:
        s.partial_page = 3
        update_partial(s)


def go_to_page_2(state):
    with state as s:
        s.partial_page = 2
        s.table = create_linear_df(
            a=state.a, b=state.b, x_min=-10, x_max=10, num_points=100
        )
        update_partial(s)


def go_to_page_1(state):
    with state as s:
        s.partial_page = 1
        update_partial(s)


def update_partial(state):

    if state.partial_page == 1:
        with tgb.Page() as a_partial:
            tgb.text("## Select a (slope) and b (intercept) values", mode="md")
            with tgb.layout("1 1"):
                tgb.number("{a}", label="select a")
                tgb.number("{b}", label="select b")
                tgb.text("")
                tgb.button(label="Next", on_action=go_to_page_2)
        state.partial_variable.update_content(state, a_partial)
    elif state.partial_page == 2:
        with tgb.Page() as a_partial:
            tgb.text("## Here is the data:", mode="md")
            tgb.table("{table}", downloadable=True)
            with tgb.layout("1 1"):
                tgb.button(label="Come back", on_action=go_to_page_1)
                tgb.button(label="Next", on_action=go_to_page_3)
        state.partial_variable.update_content(state, a_partial)
    elif state.partial_page == 3:
        with tgb.Page() as a_partial:
            tgb.text("## Here is the chart:", mode="md")
            tgb.chart("{table}", type="scatter", x="x", y="y")

            with tgb.layout("1 1"):
                tgb.button(label="Come back", on_action=go_to_page_2)
        state.partial_variable.update_content(state, a_partial)


# Define the main page layout
with tgb.Page() as main_page:
    tgb.text("# Hello from the main page!", mode="md")

    tgb.part(partial="{partial_variable}")


def on_init(state):
    update_partial(state)


if __name__ == "__main__":

    partial_page = 1
    a = 0
    b = 0
    table = pd.DataFrame(columns=["x", "y"])

    gui = Gui(main_page)
    partial_variable = gui.add_partial("")
    gui.run(dark_mode=False)  # , use_reloader=True)
