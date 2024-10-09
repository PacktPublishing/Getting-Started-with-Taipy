from multiprocessing import Value

import taipy.gui.builder as tgb
from orchestration import auto_scenario

with tgb.Page() as job_viewer:
    tgb.text("# Job viewer", mode="md")

    tgb.job_selector()
