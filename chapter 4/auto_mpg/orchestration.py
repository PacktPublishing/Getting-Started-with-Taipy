import taipy as tp
from configuration.config import predict_config, train_auto_pipeline_config
from taipy import Orchestrator


def monitor_scenario(scenario, job):
    print(f"Running scenario: '{scenario.config_id}' ||| task: '{job.task.config_id}'")


orchestrator = Orchestrator()
orchestrator.run()


training_scenario = tp.create_scenario(train_auto_pipeline_config)
predicting_scenario = tp.create_scenario(predict_config)

tp.subscribe_scenario(monitor_scenario)
