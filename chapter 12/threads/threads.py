import time
from threading import Thread

from taipy.gui import Gui
from taipy.gui import builder as tgb
from taipy.gui import get_state_id, invoke_callback, notify

initial_value = 21


def multiply(initial_value):
    time.sleep(2)
    initial_value = initial_value * 2
    return initial_value


def notify_thread_success(state, new_value):
    notify(state, "s", f"The Long Task is over")
    state.initial_value = new_value


def multiply_thread(state_id, initial_value):
    new_value = multiply(initial_value)
    invoke_callback(gui, state_id, notify_thread_success, [new_value])


def multiply_by_2(state):
    notify(state, "i", "You just triggered the Callback")
    thread = Thread(
        target=multiply_thread, args=[get_state_id(state), state.initial_value]
    )
    thread.start()


with tgb.Page() as first_long_callback:
    tgb.text("# Our first long running Callback", mode="md")

    tgb.text("Initial value is: {initial_value}")
    tgb.button("Multiply by 2", on_action=multiply_by_2)


if __name__ == "__main__":
    gui = Gui(page=first_long_callback)
    gui.run(use_reloader=True, dark_mode=False)
