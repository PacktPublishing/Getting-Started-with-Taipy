import taipy.gui.builder as tgb
from orchestration import predicting_scenario, training_scenario

with tgb.Page() as dag:

    tgb.text("## Pipeline Training DAG:", mode="md")
    tgb.scenario_dag(scenario="{training_scenario}")

    tgb.text("## Prediction DAG:", mode="md")
    tgb.scenario_dag(scenario="{predicting_scenario}")
