import taipy.gui.builder as tgb
from orchestration import auto_scenario


def print_job_info(state, var_name, value):
    print("hi")
    print(var_name)

    print(value)


with tgb.Page() as job_selector:
    tgb.text("# Job selector", mode="md")

    tgb.job_selector(show_submitted_id=True)
