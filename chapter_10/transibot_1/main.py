from algorithms.chat_algos import talk_to_bot
from langchain_mistralai.chat_models import ChatMistralAI

from taipy.gui import Gui
from taipy.gui import builder as tgb


def change_chat_status(state):
    with state as s:
        current_status = s.chat_is_active
        if current_status:
            clear_current_chat(s)

        s.chat_is_active = not current_status
        update_chat_partial(s)


def clear_current_chat(state):
    with state as s:
        s.messages = []
        s.message_history = []
        gui_to_reload = s.get_gui()
        gui_to_reload.reload()


def update_chat_partial(state):
    if state.chat_is_active:
        with tgb.Page() as active_chat_page:
            tgb.text(lambda user_name: f"## Chatting  **With** {user_name}", mode="md")
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
            tgb.button(
                label="Start chatting",
                class_name="fullwidth plain color-start",
                on_action=change_chat_status,
            )

        state.chat_partial.update_content(state, inactive_chat_page)


def chat(state, var_name: str, payload: dict):
    state.chat_element_active = False
    chat_arguments = payload.get("args", [])
    (_, _, user_message, sender_id) = chat_arguments[:4]
    messages = state.messages
    message_history = state.message_history

    messages.append((f"{len(messages)}", user_message, sender_id))
    try:
        # Send the message to the LangChain function .. And to the API.
        result, message_history = talk_to_bot(user_message, message_history, chat_bot)
        result_message = result.content
    except Exception:
        result_message = "There was a problem!"

    messages.append((f"{len(messages)}", result_message, users[1]))
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

if __name__ == "__main__":
    # Initialize chat model
    chat_name = "mistral-small"
    chat_bot = ChatMistralAI(
        model=chat_name,
    )
    message_history = []

    # Variables for chat display
    user_name = "The 🤖 TransitBot"
    users = ["User", user_name]
    messages = []

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
