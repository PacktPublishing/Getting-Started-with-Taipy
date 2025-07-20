import datetime as dt

from configuration.config_comparison import scenario_config

import taipy as tp
from taipy import Orchestrator

if __name__ == "__main__":

    Orchestrator().run()

    ##################################
    ##   Create Scenarios           ##
    ##################################

    scenario_december_1 = tp.create_scenario(
        scenario_config,
        creation_date=dt.datetime(2024, 12, 22),
        name="Scenario 1 - December",
    )
    scenario_december_2 = tp.create_scenario(
        scenario_config,
        creation_date=dt.datetime(2024, 12, 25),
        name="Scenario 2 - December",
    )
    scenario_january_1 = tp.create_scenario(
        scenario_config,
        creation_date=dt.datetime(2026, 1, 1),
        name="Scenario 1 - January",
    )
    scenario_january_2 = tp.create_scenario(
        scenario_config,
        creation_date=dt.datetime(2026, 1, 13),
        name="Scenario 2 - January",
    )

    scenario_december_1.markup_node.write(1.5)
    scenario_december_1.buying_price_node.write(2)

    scenario_december_2.markup_node.write(1.6)

    scenario_january_1.markup_node.write(1.5)
    scenario_january_1.buying_price_node.write(2.2)

    scenario_january_1.markup_node.write(1.6)

    scenario_december_1.submit()
    scenario_december_2.submit()

    # Scenario comparison

    print(tp.compare_scenarios(scenario_december_1, scenario_december_2))

    comparison = tp.compare_scenarios(scenario_december_1, scenario_december_2)
    selling_prices = comparison["selling_price_node"]["compare_price"]

    print(selling_prices)
