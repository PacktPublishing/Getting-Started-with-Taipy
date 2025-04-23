import datetime
import random

import pandas as pd
import plotly.express as px
from taipy.gui import Gui
from taipy.gui import builder as tgb

var1 = 0


df_performance = pd.DataFrame(
    columns=["variables", "time_with_with", "time_without_with"]
)


def callback_compare(state):

    df_performance_builder = df_performance.copy()
    for number_of_variables in range(1, 11):

        start_without_with = datetime.datetime.now()

        for _ in range(50):
            for _ in range(number_of_variables):
                state.var1 = random.random()
        time_without_with = datetime.datetime.now() - start_without_with
        time_without_with = time_without_with.total_seconds() * 1_000

        start_with_with = datetime.datetime.now()
        for _ in range(50):
            with state as s:
                for _ in range(number_of_variables):
                    s.var1 = random.random()

        time_with_with = datetime.datetime.now() - start_with_with
        time_with_with = time_with_with.total_seconds() * 1_000

        new_row_df = pd.DataFrame(
            {
                "variables": [number_of_variables],
                "time_with_with": [time_with_with],
                "time_without_with": [time_without_with],
            }
        )

        df_performance_builder = pd.concat(
            [df_performance_builder, new_row_df], ignore_index=True
        )

    df_performance_builder["time_with_with"] = (
        df_performance_builder["time_with_with"] / 50
    )
    df_performance_builder["time_without_with"] = (
        df_performance_builder["time_without_with"] / 50
    )

    state.df_performance = df_performance_builder


def callback_with_with(state):
    start = datetime.datetime.now()

    state.run_time_with_with = datetime.datetime.now() - start


with tgb.Page() as test_page:
    tgb.button("Compare Callbacks", on_action=callback_compare)

    with tgb.layout("1 1 1 1"):
        tgb.text("#### Var1: {var1}", mode="md")

    tgb.text(
        "### Comparison of execution time between with and without the with statement",
        mode="md",
    )

    tgb.chart(
        "{df_performance}",
        type="bar",
        x="variables",
        y__1="time_with_with",
        y__2="time_without_with",
        yaxis="average running time (ms)",
        title="Average running time (ms) using with vs not using it, for 1 to 10 variables (50 iterations in a desktop computer, results will vary with hardware)",
    )

if __name__ == "__main__":
    Gui(page=test_page).run(
        dark_mode=False,
        # use_reloader=True,
    )
