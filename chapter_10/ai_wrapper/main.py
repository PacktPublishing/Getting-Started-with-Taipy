from langchain_core.messages import HumanMessage
from langchain_mistralai.chat_models import ChatMistralAI
from taipy.gui import Gui
from taipy.gui import builder as tgb


def talk_to_bot(input_message, history, chat):
    history.append(HumanMessage(content=input_message))
    response = chat.invoke(history)
    history.append(response)
    return response, history


def chat(state, var_name: str, payload: dict):
    (_, _, user_message, sender_id) = payload.get("args", [])
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
    state.messages = messages
    state.message_history = message_history


with tgb.Page() as chat_page:
    tgb.text("# Our First **Chat** With Taipy", mode="md")
    tgb.html("hr")
    with tgb.part():
        tgb.chat(
            "{messages}",
            users="{users}",
            show_sender=True,
            sender_id="{users[0]}",
            on_action=chat,
            mode="markdown",
        )

if __name__ == "__main__":
    users = ["User", "Bot"]
    messages = []
    # Initialize chat model
    chat_name = "mistral-small"
    chat_bot = ChatMistralAI(
        model=chat_name,
    )
    message_history = []

    gui = Gui(chat_page, css_file="./css/main.css")
    gui.run(title="Simple Chat", dark_mode=False, use_reloader=True)
