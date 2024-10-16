import taipy.gui.builder as tgb
from taipy.gui import Gui

with tgb.Page() as hello_earth_python:
    tgb.text("# Hello Earth!", mode="md")

hello_mars_markdown = "# Hello Mars!"

# Comment or or the other:
page_to_run = Gui(page=hello_earth_python)
# page_to_run = Gui(page=hello_mars_markdown)

if __name__ == "__main__":

    page_to_run.run(use_reloader=True, dark_mode=False)
