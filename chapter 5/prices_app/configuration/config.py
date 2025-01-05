import datetime as dt

import pandas as pd
import taipy as tp
from algorithms.calculate_price import calculate_price
from taipy import Config, Frequency, Scope

vat_data_node_config = Config.configure_data_node(
    id="vat_node", scope=Scope.GLOBAL, default_data=1.2
)

buying_price_node_config = Config.configure_data_node(
    id="buying_price_node",
    scope=Scope.CYCLE,
)

markup_node_config = Config.configure_data_node(
    id="markup_node",
    scope=Scope.SCENARIO,
)

selling_price_node_config = Config.configure_data_node(
    id="selling_price_node",
    scope=Scope.SCENARIO,
)


calculate_price_task_config = Config.configure_task(
    id="calculate_price_task",
    function=calculate_price,
    input=[buying_price_node_config, markup_node_config, vat_data_node_config],
    output=selling_price_node_config,
)

scenario_config = Config.configure_scenario(
    id="pricing_scenario",
    task_configs=[calculate_price_task_config],
    frequency=Frequency.MONTHLY,
)
