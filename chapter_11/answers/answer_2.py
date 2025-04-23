import time

from taipy.gui import Gui
from taipy.gui import builder as tgb
from taipy.gui import invoke_long_callback, notify

value = 0
factor = 0
operation = "addition"
iteration = 0


def calculate(input_value, input_factor, input_operation):
    time.sleep(input_factor)
    if input_operation == "addition":
        result = input_value + input_factor
    elif input_operation == "substraction":
        result = input_value - input_factor
    elif input_operation == "multiplication":
        result = input_value * input_factor
    elif input_operation == "division":
        result = input_value / input_factor
    return result


jokes = [
    # jokes by Google Gemini
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my wife she was acting like a dictionary... She just flipped out.",
    "I used to have a fear of speed bumps, but I'm over the hump now.",
    "I'm on a seafood diet. I see food, and I eat it.",
    "I went to a bookstore and asked the salesperson, 'Do you have any books about paranoia?' He whispered, 'They're right behind you.'",
    "I asked a librarian for books about paranoia. She whispered, 'They're right behind you.'",
    "What do you call a lazy kangaroo? A pouch potato.",
    "I'm so good at sleeping, I can do it with my eyes closed.",
    "I'm so tired, I could sleep for a week... if only I had the energy.",
    "I'm so bad at telling jokes, I'm going to stick to riddles. They're a lot more puzzling.",
]


def update_status(state, status, result):
    state.iteration = 0
    if isinstance(status, bool):
        if status:
            if result < 0:
                result = 0
                with state as s:
                    s.value = result
                    notify(s, "w", "We Don't accept negative values, setting to 0")
            else:
                with state as s:
                    s.value = result
                    notify(s, "s", "Value updated")
        else:
            notify(state, "e", "You're not trying to divide by 0, are you?")
    else:
        print(status)
        notify(state, "i", f"Work in progress... Heres's a joke: {jokes[status]}")


def launch_operation(state):
    invoke_long_callback(
        state,
        calculate,
        [state.value, state.factor, state.operation],
        update_status,
        [],
        1000,
    )


with tgb.Page() as operation_app:
    tgb.text("# Perform simple math", mode="md")

    with tgb.layout("1 1 1"):

        tgb.selector(
            "{operation}",
            lov=["addition", "subtraction", "multiplication", "division"],
            dropdown=True,
        )

        tgb.number("{factor}", min=0, max=10)

        tgb.button("Perform Operation!", on_action=launch_operation)

    tgb.text("## Current value is: {value}", mode="md")

if __name__ == "__main__":
    gui = Gui(page=operation_app)
    gui.run(dark_mode=False)  # , use_reloader=True)
