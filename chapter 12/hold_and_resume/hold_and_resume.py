import time

from taipy.gui import Gui
from taipy.gui import builder as tgb
from taipy.gui import hold_control, notify, resume_control


def callback_with_hold(state):
    hold_control(state, message="I'm thinking hard!")
    notify(state, "i", "Callback started")
    with state as s:
        time.sleep(5)
        resume_control(s)
        notify(s, "s", "Callback finished")


with tgb.Page() as hold_and_resume_page:
    tgb.text("# Hold and Resume control!", mode="md")

    tgb.button("I'll take control away from you!", on_action=callback_with_hold)

if __name__ == "__main__":
    gui = Gui(page=hold_and_resume_page)
    gui.run(use_reloader=True, dark_mode=False)
