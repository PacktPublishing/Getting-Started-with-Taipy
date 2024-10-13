import taipy as tp
from configuration.config import predict_config, train_auto_pipeline_config
from taipy import Orchestrator

orchestrator = Orchestrator()
orchestrator.run()


training_scenario = tp.create_scenario(train_auto_pipeline_config)
predicting_scenario = tp.create_scenario(predict_config)
