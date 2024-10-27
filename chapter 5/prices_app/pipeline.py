import datetime as dt

import pandas as pd
import taipy as tp
import taipy.gui.builder as tgb
from configuration.config import scenario_config
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

    ##################################
    ##   Write input Data Nodes     ##
    ##################################

    scenario_december_1.vat_node.write(1.2)  # Not necessry because has default data
    scenario_december_1.margin_node.write(1.5)
    scenario_december_1.buying_price_node.write(2)

    print("\n Scenario submitted:")
    scenario_december_1.submit()

    price_december = scenario_december_1.selling_price_node.read()
    print(f"\nThe price for December with is {round(price_december, 2)}")

    # We didn't submit Scenario december_2, but it shares the Cycle with december_1
    # The buying_price_node should have the same value as december_1 (they are the same Data Node):

    december_buying_price = scenario_december_2.buying_price_node.read()
    print(
        f"\nThe value of december_buying_price's Data Node is: {december_buying_price}"
    )

    # If we try the same with margin_node, we'll have an error, because this Data Node doesn't exist
    # It doesn't exist because we never submitted scenario_desember_2:

    december_2_margin = scenario_december_2.margin_node.read()
    print(f"\nThe value of scenario_december_2's margin_node is {december_2_margin}")

    # Also, if we try to access the value of buying_price_node from scenario_january_1 (or _2...)
    # We will get a None value, since they belong to a different Cycle!

    january_buying_price = scenario_january_2.buying_price_node.read()
    print(f"\nThe value of january_buying_price's Data Node is: {january_buying_price}")

    ##################################
    ##   Access Cycle information   ##
    ##################################

    december_1_cycle = scenario_december_1.cycle
    print("\nThis is how december_1's cyle prints:")
    print(december_1_cycle)

    print("\nThis is december_1's creation date:")
    print(december_1_cycle.creation_date)

    print("\nThis is december_1's end date:")
    print(december_1_cycle.end_date)

    print("\nThis is december_1's start date:")
    print(december_1_cycle.start_date)

    print("\nThis is december_1's id:")
    print(december_1_cycle.id)

    print("\nThis is december_1's cycle's name:")
    print(december_1_cycle.name)

    print("\nThis is december_1's label:")
    print(december_1_cycle.get_label())

    print("\nThese are all the Cycles::")
    print(tp.get_cycles())
    cycle_1 = tp.get_cycles()[0]

    print("\nThese are all the Scenarios in the first Cycle in the list:")
    print(tp.get_scenarios(cycle=tp.get_cycles()[0]))

    ##################################
    ## Access Primary Scenario info ##
    ##################################

    print("\nThese are all the Primary Scenarios:")
    print(tp.get_primary_scenarios())

    print("\nThis is the Primary Scenario for the first Cycle of the list:")
    print(tp.get_primary(cycle_1))
