from taipy import Gui
from taipy.designer import Page

if __name__ == "__main__":
    hello = "Hello World!"
    page = Page("hello_designer.xprjson")
    Gui(page).run(design=True)
