import time

from taipy.gui import Gui
from taipy.gui import builder as tgb
from taipy.gui import invoke_long_callback, notify

initial_value = 1


def multiply(initial_value):
    time.sleep(10)  # this will force notification updates
    initial_value = initial_value * 2
    print(initial_value)
    return initial_value


def update_status(state, status, initial_value):
    if isinstance(status, bool):
        if status:
            with state as s:  # We learned this in the previous section, let's use it!
                s.initial_value = initial_value
                notify(s, "s", "the value has been updated!")
        else:
            notify(state, "e", "Oh no! the Callback failed!!")
    else:  # if not bool then it's int
        notify(state, "i", f"The Long Callback is still running... {status}")


def multiply_by_2(state):
    # invoke_long_callback(state, multiply, [state.initial_value]) # use this to NOT update status
    # invoke_long_callback(state, multiply, [state.initial_value], update_status) # Use this if you don't want periodic updates
    invoke_long_callback(
        state, multiply, [state.initial_value], update_status, [], 2000
    )


with tgb.Page() as first_long_callback:
    tgb.text("# Our first long running Callback", mode="md")

    tgb.text("Initial value is: {initial_value}")
    tgb.button("Multiply by 2", on_action=multiply_by_2)


if __name__ == "__main__":
    Gui(page=first_long_callback).run(use_reloader=True, dark_mode=False)
