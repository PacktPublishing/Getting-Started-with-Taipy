from algorithms.chat_algos import talk_to_bot
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_mistralai.chat_models import ChatMistralAI

from taipy.gui import Gui
from taipy.gui import builder as tgb


def ask_first_question(
    state,
    selected_prompt,
):
    payload = {"args": ["", "", selected_prompt, state.users[0]]}
    chat(state, "", payload)


def select_prompt(state, id):
    if id == "prompt_1":
        selected_prompt = state.user_prompt_1.content
    elif id == "prompt_2":
        selected_prompt = state.user_prompt_2.content
    elif id == "prompt_3":
        selected_prompt = state.user_prompt_3.content
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
        if id != "":
            ask_first_question(
                s,
                selected_prompt,
            )
            s.user_prompt_first_input = (
                ""  # Clear user prompt in welcome page AFTER asking
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
                        tgb.text(f"{user_prompt_1.content}", mode="md")
                        tgb.button(
                            label="Ask",
                            on_action=change_chat_status,
                            id="prompt_1",
                            class_name="fullwidth plain color-start stick-bottom",
                        )
                    with tgb.part(class_name="card-bg outer"):
                        tgb.text(f"{user_prompt_2.content}", mode="md")
                        tgb.button(
                            label="Ask",
                            on_action=change_chat_status,
                            id="prompt_2",
                            class_name="fullwidth plain color-start stick-bottom",
                        )
                    with tgb.part(class_name="card-bg outer"):
                        tgb.text(f"{user_prompt_3.content}", mode="md")
                        tgb.button(
                            label="Ask",
                            on_action=change_chat_status,
                            id="prompt_3",
                            class_name="fullwidth plain color-start stick-bottom",
                        )
            tgb.html("hr")
            with tgb.layout("1 1"):
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
    chat_arguments = payload.get("args", [])
    (_, _, user_message, sender_id) = chat_arguments[:4]
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


def on_init(state):
    update_chat_partial(state)


with tgb.Page() as chat_page:
    tgb.text("# **AI Transit Assistant**", mode="md")
    tgb.html("hr")
    tgb.part(partial="{chat_partial}", class_name="color-primary")


stylekit = {"color_primary": "#FF69B4", "color-secondary": "#EE82EE"}


def read_prompt(file_name, type):
    with open(file_name, "r") as prompt:
        prompt_text = prompt.read()

    if type == "system":
        message = SystemMessage(prompt_text)
    elif type == "human":
        message = HumanMessage(prompt_text)
    return message


if __name__ == "__main__":
    # Initialize chat model
    chat_name = "mistral-small"
    temperature = 0.6

    system_prompt = read_prompt("./prompts/system_prompt.txt", type="system")

    message_history = [system_prompt]
    chat_bot = ChatMistralAI(model=chat_name, temperature=temperature)

    # Predefined Prompts
    user_prompt_1 = read_prompt("./prompts/user_prompt_1.txt", type="human")
    user_prompt_2 = read_prompt("./prompts/user_prompt_2.txt", type="human")
    user_prompt_3 = read_prompt("./prompts/user_prompt_3.txt", type="human")

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
