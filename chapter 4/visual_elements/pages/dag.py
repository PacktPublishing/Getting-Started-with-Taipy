import taipy.gui.builder as tgb
from orchestration import auto_scenario

with tgb.Page() as dag:

    tgb.text("# Scenario DAG:", mode="md")
    tgb.scenario_dag(scenario="{auto_scenario}")
