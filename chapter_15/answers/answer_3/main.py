import base64

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from taipy import Gui
from taipy.designer import Page


def on_change(state, var, val):
    if var == "picture":
        state.picture = val
        image_data = base64.b64decode(val)

        with open("output_image.png", "wb") as f:
            f.write(image_data)


if __name__ == "__main__":
    html_hbar = "<hr>"
    picture = None
    page = Page("main.xprjson")
    Gui(page).run(design=True, title="form app", use_reloader=True)
