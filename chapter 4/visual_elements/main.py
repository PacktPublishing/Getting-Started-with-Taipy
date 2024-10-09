import taipy as tp
import taipy.gui.builder as tgb
from pages.dag import dag
from pages.job_viewer import job_viewer
from pages.regular_ui import regular_ui
from pages.scenario_selector import scenario_selector
from pages.scenario_viewer import scenario_viewer
from taipy import Gui

with tgb.Page() as root_page:
    tgb.text("# Auto-mpg app", mode="md")
    tgb.navbar()


auto_mpg_pages = {
    "/": root_page,
    "regular_ui": regular_ui,
    "dag": dag,
    "scenario_viewer": scenario_viewer,
    "scenario_selector": scenario_selector,
    "job_viewer": job_viewer,
}


auto_mpg_gui = Gui(pages=auto_mpg_pages)


auto_mpg_gui.run(
    use_reloader=True,
    dark_mode=False,
    title="Data Node examples",
)
