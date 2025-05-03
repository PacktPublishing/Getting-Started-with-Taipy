import json

from algorithms.chat_algos import talk_to_bot
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_mistralai.chat_models import ChatMistralAI
from taipy.gui import Gui
from taipy.gui import builder as tgb
from taipy.gui import invoke_long_callback


def ask_first_question(
    state,
    selected_prompt,
):
    payload = {"args": ["", "", selected_prompt, state.users[0]]}
    chat(state, "", payload)


### ANSWER 2: Essential function
def ask_and_answer_first_question(
    state,
    selected_prompt,
):
    answer = all_qa.get(selected_prompt)

    with state as s:
        messages = s.messages
        message_history = s.message_history
        users = s.users
        sender_id = s.users[0]

    messages.append((f"{len(messages)}", selected_prompt, sender_id))
    messages.append((f"{len(messages)}", answer, users[1]))

    message_history.append(HumanMessage(selected_prompt))
    message_history.append(AIMessage(answer))


def select_prompt(state, id):
    if id == "prompt_1":
        selected_prompt = state.user_prompt_1
    elif id == "prompt_2":
        selected_prompt = state.user_prompt_2
    elif id == "prompt_3":
        selected_prompt = state.user_prompt_3
    elif id == "user_custom_message":
        selected_prompt = state.user_prompt_first_input
    else:
        selected_prompt = None
    return selected_prompt


def change_chat_status(state, id, payload):
    selected_prompt = select_prompt(state, id)

    if id != "" and selected_prompt == "":
        return

    with state as s:
        current_status = s.chat_is_active
        if current_status:
            clear_current_chat(s)

        s.chat_is_active = not current_status
        update_chat_partial(s)
        if id == "user_custom_message":
            ask_first_question(
                s,
                selected_prompt,
            )
            s.user_prompt_first_input = (
                ""  # Clear user prompt in welcome page AFTER asking
            )
        elif id != "":
            ask_and_answer_first_question(
                s,
                selected_prompt,
            )


def clear_current_chat(state):
    with state as s:
        s.messages = []
        s.message_history = [
            s.system_prompt
        ]  # Always add the system prompt to the beginiing of the conversation
        gui_to_reload = s.get_gui()
        gui_to_reload.reload()


def change_model(state):
    with state as s:
        model_name = models.get(s.bot_name)
        s.users = ["User", s.bot_name]

        new_bot = ChatMistralAI(model=model_name, temperature=s.temperature)
        s.chat_bot = new_bot


def update_chat_partial(state):
    if state.chat_is_active:
        with tgb.Page() as active_chat_page:
            tgb.text(lambda bot_name: f"## Chatting  **With** {bot_name}", mode="md")
            tgb.chat(
                "{messages}",
                users="{users}",
                show_sender=True,
                sender_id="{users[0]}",
                on_action=chat,
                mode="markdown",
                active="{chat_element_active}",
            )
            with tgb.layout("1 1"):
                tgb.button(
                    label="New chat",
                    class_name="fullwidth plain color-new",
                    on_action=change_chat_status,
                )
                tgb.button(
                    label="Clear Chat",
                    class_name="fullwidth plain color-clear",
                    on_action=clear_current_chat,
                )
        state.chat_partial.update_content(state, active_chat_page)
    else:

        with tgb.Page() as inactive_chat_page:
            tgb.text("## Start **New** Chat!", mode="md")
            tgb.html("hr")

            with tgb.part() as questions_part:
                with tgb.layout("1 1 1"):
                    with tgb.part(class_name="card-bg outer"):
                        tgb.text(
                            user_prompt_1, mode="md"
                        )  # We don't use .content because this is not a HumanMessage anymore
                        tgb.button(
                            label="Ask",
                            on_action=change_chat_status,
                            id="prompt_1",
                            class_name="fullwidth plain color-start stick-bottom",
                        )
                    with tgb.part(class_name="card-bg outer"):
                        tgb.text(user_prompt_2, mode="md")
                        tgb.button(
                            label="Ask",
                            on_action=change_chat_status,
                            id="prompt_2",
                            class_name="fullwidth plain color-start stick-bottom",
                        )
                    with tgb.part(class_name="card-bg outer"):
                        tgb.text(user_prompt_3, mode="md")
                        tgb.button(
                            label="Ask",
                            on_action=change_chat_status,
                            id="prompt_3",
                            class_name="fullwidth plain color-start stick-bottom",
                        )
            tgb.html("hr")
            with tgb.layout("1 1 1"):
                with tgb.part():
                    tgb.text("Select **Bot** Creativity", mode="md")
                    tgb.slider(
                        value="{temperature}",
                        min=0,
                        max=1,
                        step=0.1,
                        on_change=change_model,
                        labels={
                            0.0: "🧐 ",
                            1.0: "🤪",
                        },
                        hover_text="Higher Values make the assistant more creative",
                    )
                tgb.selector(
                    value="{bot_name}",
                    lov="{chat_bots}",
                    dropdown=True,
                    on_change=change_model,
                    label="Select your Assistant",
                )
                tgb.selector(
                    value="{transibot_style}",
                    lov="{transibot_styles}",
                    dropdown=True,
                    on_change=change_system_prompt,
                    label="Select your Assistant's style",
                )
            tgb.input(
                value="{user_prompt_first_input}",
                label="Ask your Question!",
                multiline=True,
                class_name="fullwidth",
                id="user_custom_message",
                on_action=change_chat_status,
            )
            tgb.button(
                label="Ask",
                class_name="fullwidth plain color-start",
                id="user_custom_message",
                on_action=change_chat_status,
            )

        state.chat_partial.update_content(state, inactive_chat_page)


def chat(state, var_name: str, payload: dict):
    state.chat_element_active = False
    (_, _, user_message, sender_id) = payload.get("args", [])
    if user_message == "":
        return
    with state as s:
        messages = s.messages
        message_history = s.message_history
        users = s.users
        bot = s.chat_bot

    messages.append((f"{len(messages)}", user_message, sender_id))
    try:
        # Send the message to the LangChain function .. And to the API.
        result, message_history = talk_to_bot(user_message, message_history, bot)
        result_message = result.content
    except Exception:
        result_message = "There was a problem!"

    messages.append((f"{len(messages)}", result_message, users[1]))
    print(message_history)
    with state as s:
        s.messages = messages
        s.message_history = message_history
        s.chat_element_active = True


with tgb.Page() as chat_page:
    tgb.text("# **AI Transit Assistant**", mode="md")
    tgb.html("hr")
    tgb.part(partial="{chat_partial}", class_name="color-primary")


stylekit = {"color_primary": "#FF69B4", "color-secondary": "#EE82EE"}


def read_system_prompt(file_name):
    with open(file_name, "r") as prompt:
        prompt_text = prompt.read()

    message = SystemMessage(prompt_text)
    return message


def read_question_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        question = data.get("question")
        answer = data.get("answer")
        return {question: answer}


def change_system_prompt(state):
    with state as s:
        prompt_address = transibot_style_prompts.get(s.transibot_style)
        s.system_prompt = read_system_prompt(prompt_address)
        s.message_history = [s.system_prompt]


def on_init(state):
    update_chat_partial(state)


if __name__ == "__main__":
    # Initialize chat model
    chat_name = "mistral-small"
    temperature = 0.6

    chat_bot = ChatMistralAI(model=chat_name, temperature=temperature)

    # ANSWER 2, changes here (and in the prompt files!)
    all_qa = {}
    all_qa.update(read_question_from_json("./prompts/user_prompt_1.json"))
    all_qa.update(read_question_from_json("./prompts/user_prompt_2.json"))
    all_qa.update(read_question_from_json("./prompts/user_prompt_3.json"))
    user_prompt_1, user_prompt_2, user_prompt_3 = all_qa.keys()

    user_prompt_first_input = ""

    # Variables for chat display
    bot_name = "The 🤖 TransitBot"
    users = ["User", bot_name]
    messages = []

    models = {
        "The 🤖 TransitBot": "mistral-small",
        "The 🤖 TransitBot 🦾 PLUS": "mistral-large-latest",
    }
    chat_bots = list(models.keys())

    ### ANSWER 2/ Variables for System Prompt change
    transibot_style_prompts = {
        "neutral": "./prompts/system_prompt.txt",
        "brooklyn": "./prompts/system_prompt_brooklyn.txt",
    }
    transibot_styles = list(transibot_style_prompts.keys())
    transibot_style = transibot_styles[0]
    system_prompt = read_system_prompt(transibot_style_prompts.get(transibot_style))

    message_history = [system_prompt]

    # Variable for partial:
    chat_is_active = False

    # Variable for the chat element
    chat_element_active = True

    gui = Gui(chat_page, css_file="./css/main.css")
    chat_partial = gui.add_partial(page="")
    gui.run(
        title="The TransiBot",
        favicon="./img/chat_favicon.ico",
        dark_mode=False,
        stylekit=stylekit,
        use_reloader=True,
    )
