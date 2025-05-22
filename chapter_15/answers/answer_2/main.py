import pandas as pd
from taipy import Gui
from taipy.designer import Page


def clear_variable(state):
    with state as s:
        s.description = ""
        s.price = 0
        print(s.price)


def add_to_dataframe(state):
    with state as s:
        if s.description == "":
            print("no description")
            return
        elif s.price == 0:
            "price has to be > 0"
            return
        list_to_append = [[s.selected_item, s.description, s.price]]
        new_row = pd.DataFrame(
            list_to_append, columns=["selected_item", "description", "price"]
        )
        s.df_items = pd.concat([s.df_items, new_row], ignore_index=True)
        print(s.df_items.head())
    # After updating the DataFrame:
    with state as s:
        clear_variable(s)
    state.refresh("df_items")
    state.refresh("description")
    state.refresh("price")


if __name__ == "__main__":
    items = [
        "Bluetooth speaker",
        "VR headset",
        "camera",
        "computer",
        "drone",
        "e-reader",
        "external hard drive",
        "gaming console",
        "GPS device",
        "headphones",
        "laptop",
        "printer",
        "projector",
        "smart TV",
        "smartphone",
        "smartwatch",
        "tablet",
        "webcam",
    ]
    selected_item = items[0]
    description = ""
    df_items = pd.DataFrame(columns=["selected_item", "description", "price"])
    price = 0
    page = Page("main.xprjson")
    Gui(page).run()  # design=True, title="form app", use_reloader=True)
