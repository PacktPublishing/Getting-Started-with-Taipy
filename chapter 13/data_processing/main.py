
import taipy.gui.builder as tgb
from taipy.gui import Gui
import taipy as tp

from configuration.config import download_scenario_config

from taipy.gui import State, hold_control, resume_control
from pathlib import Path


import datetime as dt

from taipy import Orchestrator
from io import BytesIO
import pandas as pd


def update_data(state):
    state.df_month= update_month(state.selected_month)

with tgb.Page() as cache_analyze_page:
    tgb.text("# Analyzing and caching some files!", mode="md")

    tgb.selector(value="{selected_month}", 
                    lov = list(range(1, 13)), 
                    on_change= update_data, 
                    dropdown=True
    ) 

    tgb.table("{df_month}", rebuild=True)

if __name__=="__main__":

    Orchestrator().run() 

    selected_month = 1
    download_scenario = tp.create_scenario(download_scenario_config)
 
    def update_month(month):
        download_scenario.submit() # Download data if required
        selected_month_str = str(month).zfill(2)
        df_month = pd.read_parquet(f"./data/raw_data/yellow_tripdata_2023-{selected_month_str}.parquet")
        return df_month

    df_month = update_month(selected_month)

    gui = Gui(page=cache_analyze_page) 
    
    gui.run(dark_mode = False,  use_reloader=True)