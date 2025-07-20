from algorithms.chat_algos import (
    create_display_list,
    generate_history_metadata,
    get_users,
    load_history,
    save_history,
    talk_to_bot,
)
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_mistralai.chat_models import ChatMistralAI
from taipy.gui import builder as tgb


def update_chat_partial(state):
    if state.chat_is_active:
        with tgb.Page() as active_chat_page:
            with tgb.layout("5 1", columns__mobile="1"):
                tgb.text(
                    lambda bot_name: f"## Chatting  **With** {bot_name}", mode="md"
                )
                tgb.button(
                    "Show History", on_action=lambda s: s.assign("open_pane", True)
                )
            tgb.chat(
                "{messages}",
                users="{users}",
                show_sender=True,
                sender_id="{users[0]}",
                on_action=chat,
                mode="markdown",
                active="{chat_element_active}",
            )
            tgb.button(
                label="New chat",
                class_name="fullwidth plain color-new",
                on_action=change_chat_status,
            )
        state.chat_partial.update_content(state, active_chat_page)
    else:

        with tgb.Page() as inactive_chat_page:
            with tgb.layout("5 1", columns__mobile="1"):
                tgb.text("## Start **New** Chat!", mode="md")
                tgb.button(
                    "Show History", on_action=lambda s: s.assign("open_pane", True)
                )
            tgb.html("hr")

            with tgb.part() as questions_part:
                with tgb.layout("1 1 1"):
                    with tgb.part(class_name="card-bg outer"):
                        tgb.text("{user_prompt_1}", mode="md")
                        tgb.button(
                            label="Ask",
                            on_action=change_chat_status,
                            id="prompt_1",
                            class_name="fullwidth plain color-start stick-bottom",
                        )
                    with tgb.part(class_name="card-bg outer"):
                        tgb.text("{user_prompt_2}", mode="md")
                        tgb.button(
                            label="Ask",
                            on_action=change_chat_status,
                            id="prompt_2",
                            class_name="fullwidth plain color-start stick-bottom",
                        )
                    with tgb.part(class_name="card-bg outer"):
                        tgb.text("{user_prompt_3}", mode="md")
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


def change_model(state):
    with state as s:
        model_name = s.models.get(s.bot_name)
        s.users = ["User", s.bot_name]

        new_bot = ChatMistralAI(model=model_name, temperature=s.temperature)
        s.chat_bot = new_bot


def ask_first_question(
    state,
    selected_prompt,
):
    message_history = generate_history_metadata(
        selected_prompt,
        state.users[0],
        state.bot_name,
        state.temperature,
    )
    history = state.list_history
    history.append(message_history.name)
    state.history_file_name = message_history.filename
    system_prompt = state.message_history[0]
    save_history(system_prompt, state.history_file_name)

    with state as s:
        s.selected_history = message_history.name
        s.list_history = history
        payload = {"args": ["", "", selected_prompt, s.users[0]]}
        chat(s, "", payload)


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
        ]  # Always add the system prompt to the beginning of the conversation
        gui_to_reload = s.get_gui()
        gui_to_reload.reload()


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
        result, message_history = talk_to_bot(
            user_message, message_history, bot, state.history_file_name
        )
        result_message = result.content
    except Exception:
        result_message = "There was a problem!"

    messages.append((f"{len(messages)}", result_message, users[1]))
    with state as s:
        s.messages = messages
        s.message_history = message_history
        s.chat_element_active = True


def change_history(state):
    with state as s:
        selected_file_name = f"./history/{s.selected_history}.ndjson"
        s.message_history = load_history(selected_file_name)
        sender, s.bot_name, s.temperature = get_users(selected_file_name)
        change_model(s)
        s.messages = create_display_list(s.message_history, sender, s.bot_name)
        if not s.chat_is_active:
            s.chat_is_active = True
            update_chat_partial(s)


def read_prompt(file_name, type):
    with open(file_name, "r") as prompt:
        prompt_text = prompt.read()

    if type == "system":
        message = SystemMessage(prompt_text)
    elif type == "human":
        message = HumanMessage(prompt_text)
    return message


with tgb.Page() as chat_page:
    with tgb.pane(
        open="{open_pane}",
        on_close=lambda s: s.assign("open_pane", False),
        width="45vw",
    ):
        tgb.selector(
            value="{selected_history}",
            lov="{list_history}",
            mode="radio",
            on_change=change_history,
        )
    tgb.part(partial="{chat_partial}", class_name="color-primary")
