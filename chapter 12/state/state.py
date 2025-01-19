import datetime
import random

from taipy.gui import Gui
from taipy.gui import builder as tgb

var1 = 0
var2 = 0
var3 = 0
var4 = 0

run_time_with_with = 0
run_time_without_with = 0


def callback_without_with(state):
    start = datetime.datetime.now()
    for _ in range(1_000):
        state.var1 = random.random()
        state.var2 = random.random()
        state.var3 = random.random()
        state.var4 = random.random()
    state.run_time_without_with = datetime.datetime.now() - start


def callback_with_with(state):
    start = datetime.datetime.now()
    for _ in range(1_000):
        with state as s:
            s.var1 = random.random()
            s.var2 = random.random()
            s.var3 = random.random()
            s.var4 = random.random()
    state.run_time_with_with = datetime.datetime.now() - start


with tgb.Page() as test_page:
    with tgb.layout("1 1"):
        tgb.button("callback without with", on_action=callback_without_with)
        tgb.button("callback with with", on_action=callback_with_with)

    with tgb.layout("1 1 1 1"):
        tgb.text("#### Var1: {var1}", mode="md")
        tgb.text("#### Var2: {var2}", mode="md")
        tgb.text("#### Var3: {var3}", mode="md")
        tgb.text("#### Var4: {var4}", mode="md")

    tgb.text(
        "### Comparison of execution time for 1,000 iterations of 4 random() assignements and visual display",
        mode="md",
    )
    with tgb.layout("1 1"):
        tgb.text("#### Without 'with': {run_time_without_with}", mode="md")
        tgb.text("#### With 'with': {run_time_with_with}", mode="md")

if __name__ == "__main__":
    gui = Gui(page=test_page)
    gui.run(use_reloader=True, dark_mode=False)
