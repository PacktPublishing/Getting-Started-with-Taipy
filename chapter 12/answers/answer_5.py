import pandas as pd
import taipy as tp
import taipy.gui.builder as tgb
from taipy import Config, Gui, Orchestrator
from taipy.gui import hold_control, resume_control

rate_1 = 0
rate_2 = 0

rate_fig = 0
rate_2_fig = 0
investment = 0

df_coumpounded = None
display_chart = False


def calculate_compound_interest(interest_rate, amount, years=30):

    interest_rate = interest_rate / 100
    if interest_rate < 0:
        raise ValueError("Interest rate can't be negative.")

    df_coumpounded = pd.DataFrame({"year": range(1, years + 1)})
    df_coumpounded["total_amount"] = (
        amount * (1 + interest_rate) ** df_coumpounded["year"]
    )
    return df_coumpounded


def compare_scenarios(state):
    with state as s:
        hold_control(s)
        s.compound_scenario_1.rate.write(s.rate_1)
        s.compound_scenario_2.rate.write(s.rate_2)
        s.compound_scenario_1.investment.write(s.investment)
        s.compound_scenario_2.investment.write(s.investment)

    state.compound_scenario_1.submit(wait=True)
    state.compound_scenario_2.submit(wait=True)

    with state as s:
        df_coumpounded_1 = s.compound_scenario_1.df_compounded.read()
        df_coumpounded_2 = s.compound_scenario_2.df_compounded.read()
        df_coumpounded = df_coumpounded_1.rename(columns={"total_amount": "scenario_1"})
        df_coumpounded["scenario_2"] = df_coumpounded_2["total_amount"]
        s.df_coumpounded = df_coumpounded
        generate_results(s)
    resume_control(state)


def generate_results(state):
    if state.display_chart:
        with tgb.Page() as results_Page:
            tgb.chart(
                "{df_coumpounded}",
                type="scatter",
                x="year",
                y__1="scenario_1",
                y__2="scenario_2",
            )
        state.partial_results.update_content(state, results_Page)
    else:
        with tgb.Page() as results_Page:
            tgb.text("### Results for Scenario 1 and 2", mode="md")
            tgb.table(
                "{df_coumpounded}",
            )
        state.partial_results.update_content(state, results_Page)


with tgb.Page() as compound_interest_page:
    tgb.text("# Compare Compoud Interests", mode="md")

    with tgb.layout("1 1 1"):
        tgb.number("{investment}", label="Select your invested amount", min=0)
        tgb.button("Compare!", on_action=compare_scenarios)
        tgb.toggle(
            "{display_chart}",
            label="Display results as chart",
            on_change=generate_results,
        )

    with tgb.layout("1 1"):
        tgb.text("## Scenario 1", mode="md")
        tgb.text("## Scenario 2", mode="md")

        tgb.number(
            "{rate_1}", label="Select Rate for Scenario 1", min=0, max=15, step=0.1
        )
        tgb.number(
            "{rate_2}", label="Select Rate for Scenario 2", min=0, max=15, step=0.1
        )

    ####### Results #######
    tgb.part(partial="{partial_results}")


if __name__ == "__main__":

    Config.configure_job_executions(mode="standalone", max_nb_of_workers=2)

    # Data Nodes
    rate_node_config = Config.configure_data_node("rate")
    investment_node_config = Config.configure_data_node("investment", default_data=1)

    df_coumpounded_node_config = Config.configure_data_node("df_compounded")

    # Tasks
    calculate_compounded_task = Config.configure_task(
        id="calculate_compounded",
        function=calculate_compound_interest,
        input=[rate_node_config, investment_node_config],
        output=df_coumpounded_node_config,
    )

    # Configuration
    scenario_config = Config.configure_scenario(
        id="my_scenario", task_configs=[calculate_compounded_task]
    )
    Config.export("config_answer_5.toml")

    Orchestrator().run()

    compound_scenario_1 = tp.create_scenario(scenario_config)
    compound_scenario_2 = tp.create_scenario(scenario_config)

    # Run to start a server
    gui = Gui(page=compound_interest_page)
    partial_results = gui.add_partial(page=" ")

    gui.run(dark_mode=False)  # , use_reloader=True)
