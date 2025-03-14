import numpy as np
import pandas as pd
from taipy.gui import Gui
from taipy.gui import builder as tgb
from taipy.gui.data.decimator import LTTB, RDP, MinMaxDecimator

NOP = 200
min_max_decimator = MinMaxDecimator(n_out=NOP)
lttb_decimator = LTTB(n_out=NOP)
rdp_decimator = RDP(n_out=NOP)

with tgb.Page() as decimator_page:
    tgb.text("# Compare decimator algortihms", mode="md")

    tgb.text("## Chart without Decimator:", mode="md")
    tgb.chart(data="{df_sin}", x="x", y="y")

    tgb.text("## Chart with Min-Max Decimator:", mode="md")
    tgb.chart(data="{df_sin}", x="x", y="y", decimator="min_max_decimator")

    tgb.text("## Chart with LTTB:", mode="md")
    tgb.chart(data="{df_sin}", x="x", y="y", decimator="lttb_decimator")

    tgb.text("## Chart with RDP:", mode="md")
    tgb.chart(data="{df_sin}", x="x", y="y", decimator="rdp_decimator")


if __name__ == "__main__":
    x = np.linspace(0, 10, 100000)
    y = np.sin(x) + 0.1 * np.random.randn(100000)
    df_sin = pd.DataFrame({"x": x, "y": y})

    gui = Gui(page=decimator_page)

    gui.run(dark_mode=False, use_reloader=True)
