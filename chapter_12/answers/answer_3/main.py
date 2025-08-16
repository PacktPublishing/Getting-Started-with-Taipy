from configuration.config import analyze_scenario_config

import taipy as tp
import taipy.gui.builder as tgb
from taipy import Orchestrator
from taipy.gui import Gui
from taipy.gui.data.decimator import LTTB, RDP, MinMaxDecimator

NOP = 5000
# min_max_decimator = MinMaxDecimator(n_out=NOP)
rdp_decimator = RDP(n_out=NOP)
# lttb_decimator = LTTB(n_out=NOP)


with tgb.Page() as cache_analyze_page:
    tgb.text("# Tip Analytic", mode="md")

    # with tgb.layout("1 1 1"):
    #     with tgb.part("card"):
    #         tgb.text("## Total Tips (cc):", mode="md", class_name="color-primary")
    #         tgb.text("### $ {'{:,.0f}'.format(total_tips)}", mode="md", class_name="color-secondary")
    #     with tgb.part("card"):
    #         tgb.text("## Average Tip:", mode="md", class_name="color-primary")
    #         tgb.text("### $ {avg_tip}", mode="md", class_name="color-secondary")
    #     with tgb.part("card"):
    #         tgb.text("## Rides without tip:", mode="md", class_name="color-primary")
    #         tgb.text("### {percentage_no_tip} %", mode="md", class_name="color-secondary")
    # with tgb.layout("1 1"):
    #     tgb.chart("{df_weekend}", type="bar", x="is_weekend", y="average_tip", rebuild=True)
    #     tgb.chart("{df_night}", type="bar", x="is_night", y="average_tip", rebuild=True)
    #     tgb.chart("{df_hour}", type="bar", x="hour_of_day", y="average_tip", rebuild=True)
    #     tgb.chart("{df_from_airport}", type="bar", x="airport_fee_binary", y="average_tip", rebuild=True)

    tgb.table("{df_location}")

    # tgb.chart("{tip_and_pickup}",
    #         x="tip_date",
    #         y="tip_amount",
    #         type="scatter",
    #         mode="markers",
    #         title = "Daily tips between $20 and $100",
    #         decimator="rdp_decimator")


if __name__ == "__main__":

    Orchestrator().run()

    selected_month = 1
    analyze_scenario = tp.create_scenario(analyze_scenario_config)

    analyze_scenario.submit()

    total_tips = analyze_scenario.total_tips.read()
    avg_tip = analyze_scenario.avg_tip.read()
    percentage_no_tip = analyze_scenario.percentage_no_tip.read()
    df_weekend = analyze_scenario.df_weekend.read()
    df_night = analyze_scenario.df_night.read()
    df_hour = analyze_scenario.df_hour.read()
    df_from_airport = analyze_scenario.df_from_airport.read()

    df_location = analyze_scenario.df_location.read()  ########## Add this!

    tip_and_pickup = analyze_scenario.tip_and_pickup.read()

    gui = Gui(page=cache_analyze_page)

    gui.run(dark_mode=False)  # ,  use_reloader=True)
