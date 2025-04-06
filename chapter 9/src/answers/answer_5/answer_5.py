import taipy.gui.builder as tgb
from pages.calculate_ndvi.charts import plot_ndvi


def create_comp_partial(state):
    if state.selected_arrays:
        number_of_scenaios = len(state.selected_arrays)
        variable_layout = "1 " * number_of_scenaios
        variable_layout = variable_layout[:-1]  # we remove he last space

        with tgb.Page() as comparison:
            tgb.text("## Comparing Years", mode="md")
            with tgb.layout(variable_layout):
                for index in range(number_of_scenaios):
                    tgb.chart(
                        figure=lambda state: plot_ndvi(
                            state.selected_arrays[index],
                            state.scenario_comp_names[index],
                        )
                    )
        #                    tgb.chart(figure= lambda state : state.ndvi_images[index])

        state.answer_5_partial.update_content(state, comparison)
