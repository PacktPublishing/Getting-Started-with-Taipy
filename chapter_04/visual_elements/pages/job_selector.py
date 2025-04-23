import taipy.gui.builder as tgb
from taipy.gui import notify


def notify_job_info(state, var_name, value):
    notify(state, message=f"Selected Job: {state.selected_job}")


with tgb.Page() as job_selector:
    tgb.text("# Job selector", mode="md")

    tgb.job_selector(
        "{selected_job}",
        show_submitted_id=True,
        on_change=notify_job_info,
    )
