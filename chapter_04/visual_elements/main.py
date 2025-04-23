import taipy as tp
import taipy.gui.builder as tgb
from configuration.config import auto_scenario_config
from pages.dag import dag
from pages.job_selector import job_selector
from pages.regular_ui import regular_ui
from pages.scenario_element import scenario_element
from pages.scenario_selector import scenario_selector
from taipy import Gui, Orchestrator

with tgb.Page() as root_page:
    tgb.text("# Auto-mpg app", mode="md")
    tgb.navbar()


auto_mpg_pages = {
    "/": root_page,
    "regular_ui": regular_ui,
    "dag": dag,
    "scenario_element": scenario_element,
    "scenario_selector": scenario_selector,
    "job_selector": job_selector,
}


auto_mpg_gui = Gui(pages=auto_mpg_pages)

if __name__ == "__main__":

    orchestrator = Orchestrator()
    orchestrator.run()

    auto_scenario = tp.create_scenario(auto_scenario_config)
    selected_scenario = auto_scenario

    selected_job = None

    auto_mpg_gui.run(
        use_reloader=True,
        dark_mode=False,
        title="Data Node examples",
    )
