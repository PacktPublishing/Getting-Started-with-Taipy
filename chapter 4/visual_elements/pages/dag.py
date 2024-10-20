import taipy.gui.builder as tgb

with tgb.Page() as dag:

    tgb.text("# Scenario DAG:", mode="md")
    tgb.scenario_dag(scenario="{auto_scenario}")
