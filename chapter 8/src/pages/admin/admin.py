import taipy as tp
import taipy.gui.builder as tgb

with tgb.Page() as admin_page:

    tgb.text("# **Admin** Page", mode="md")

    tgb.html("hr")

    tgb.text(
        "Control, visualize and **monitor** the applications and its data.", mode="md"
    )

    tgb.text("### Scenario section", mode="md")
    with tgb.layout("1 4", columns__mobile="1"):
        with tgb.part("sidebar"):
            tgb.scenario_selector("{admin_scenario}", show_add_button=False)

        with tgb.part("main"):
            tgb.scenario("{admin_scenario}", show_submit=False, show_sequences=False)

            tgb.scenario_dag("{admin_scenario}")
            tgb.job_selector()

    tgb.text("### Data Node section", mode="md")

    with tgb.layout("20 80", columns__mobile="1"):
        with tgb.part("sidebar"):
            tgb.data_node_selector("{admin_data_node}")

        with tgb.part("main"):
            tgb.data_node(
                "{admin_data_node}", width="100%", file_upload=True, file_download=True
            )
