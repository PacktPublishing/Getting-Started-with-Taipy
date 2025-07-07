from taipy.gui import Gui
from taipy.gui import builder as tgb


def update_partial(state):
    with tgb.Page() as a_partial:
        tgb.text("# I'm a text inside a Partial!", mode="md")
        tgb.text("#### x has a value of {x}", mode="md")
        tgb.text("#### y has a value of {y}", mode="md")
    state.partial_variable.update_content(state, a_partial)


def update_x(state):
    new_y = state.x
    new_x = state.y + state.x
    state.x = new_x
    state.y = new_y

    if new_y > 10:
        update_partial(state)


# Define the main page layout
with tgb.Page() as main_page:
    tgb.text("# Hello from the main page!", mode="md")
    tgb.button("update x", on_action=update_x)

    tgb.part(partial="{partial_variable}")  # First Partial here

    tgb.text("## This is also in the main page!", mode="md")
    tgb.text("#### x outside the partial has a value of {x}", mode="md")

    # reuse the partial:
    tgb.part(partial="{partial_variable}", class_name="color-primary")
    tgb.part(partial="{partial_variable}", class_name="color-secondary")


with tgb.Page() as a_partial:
    tgb.text("# I'm a text inside a Partial!", mode="md")
    tgb.text("#### x has a value of {x}", mode="md")
    tgb.text("#### I won't show y until it's more than 10!", mode="md")

# Uncomment to initialize Partial from function:
# def on_init(state):
#    update_partial(state)

if __name__ == "__main__":

    x = 2
    y = 1

    gui = Gui(main_page)
    partial_variable = gui.add_partial(page=a_partial)
    gui.run(use_reloader=True, dark_mode=False)
