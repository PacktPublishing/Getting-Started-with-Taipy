import taipy as tp
import taipy.gui.builder as tgb
from flask import Flask
from taipy import Config, Gui, Orchestrator

flask_app = Flask(__name__)


def say_hi(person):
    return f"hi {person}!"


node_config_input = Config.configure_data_node(
    id="node_in",
    default_data="Flask",
)
node_config_output = Config.configure_data_node(
    id="node_out",
)
task_config = Config.configure_task(
    id="task", input=node_config_input, output=node_config_output, function=say_hi
)

scenario_config = Config.configure_scenario(id="node", task_configs=[task_config])

with tgb.Page() as page:
    tgb.text("# A Taipy app", mode="md")
    tgb.text("## {node_message}", mode="md")


@flask_app.route("/home")
def home_page():
    return "<h1>The home page.</h1>"


@flask_app.route("/contact")
def contact_page():
    return "<h1>The contact page.</h1>"


if __name__ == "__main__":
    Orchestrator().run()
    scenario = tp.create_scenario(scenario_config)
    scenario.submit()
    node_message = scenario.node_out.read()
    gui = Gui(page=page, flask=flask_app)
    gui.run()
