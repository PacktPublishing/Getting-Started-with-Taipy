import taipy as tp
import taipy.gui.builder as tgb
from pages.dag import dag
from pages.make_predictions import make_predictions
from pages.train_model import train_model
from taipy import Gui

columns_lov = [
    "cylinders",
    "displacement",
    "horsepower",
    "weight",
    "acceleration",
    "model year",
    "origin",
]
selected_columns = columns_lov


show_cylinders = True
show_displacement = True
show_horsepower = True
show_weight = True
show_acceleration = True
show_model_year = True
show_origin = True


with tgb.Page() as root_page:
    tgb.text("# Auto-mpg app", mode="md")
    tgb.navbar()


auto_mpg_pages = {
    "/": root_page,
    "train_model": train_model,
    "make_predictions": make_predictions,
    "dag": dag,
}


auto_mpg_gui = Gui(pages=auto_mpg_pages)


auto_mpg_gui.run(
    use_reloader=True,
    dark_mode=False,
    title="Data Node examples",
)
