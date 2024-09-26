from datetime import datetime

from taipy.gui import Gui
from welcome_page import welcome_page

taipy_food_gui = Gui(page=welcome_page)

taipy_food_gui.run(
    use_reloader=True,
    dark_mode=False,
    title="Taipy Food 🍜",
    favicon="./images/favicon_burger.png",
    watermark="Taipy food",
)
