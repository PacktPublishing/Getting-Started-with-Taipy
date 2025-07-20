import base64

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_mistralai.chat_models import ChatMistralAI
from taipy.gui import Gui
from taipy.gui import builder as tgb


def create_uri(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded_image}"


def analyze_image(
    uri_or_url,
    system_prompt=None,
    text="Please describe the scene in this image:",
    model_name="pixtral-12b-2409",
    temperature=0.6,
):
    chat_bot = ChatMistralAI(model=model_name, temperature=temperature)
    message_history = []

    if system_prompt:
        message_history.append(system_prompt)

    message = HumanMessage(
        content=[
            {"type": "text", "text": text},
            {"type": "image_url", "image_url": uri_or_url},
        ]
    )
    message_history.append(message)

    return chat_bot.invoke(message_history)


def load_system_prompt(filename):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
    return SystemMessage(content=content)


def submit_url(state):
    print(state.url)
    if state.url != "":
        response = analyze_image(state.url, system_prompt=system_prompt)
        state.image_description = response.content


def submit_file(state):
    image_uri = create_uri(state.file_address)
    response = analyze_image(image_uri, system_prompt=system_prompt)
    state.image_description = response.content


with tgb.Page() as chat_page:
    tgb.text("# **AI Image Description**", mode="md")
    tgb.html("hr")
    with tgb.layout("3 1 3"):
        with tgb.part():
            tgb.text("### Enter your image's URL", mode="md")
            tgb.input(
                value="{url}",
                label="Enter URL",
                class_name="fullwidth",
            )
            tgb.button(
                label="Submit",
                on_action=submit_url,
                class_name="fullwidth",
            )
        tgb.text("**OR**", mode="md")
        with tgb.part():
            tgb.text("### Upload a file:", mode="md")
            tgb.file_selector(
                content="{file_address}",
                label="Upload_file",
                extensions=".png,.jpeg,.jpg",
                on_action=submit_file,
                class_name="fullwidth",
            )

    tgb.text("## Result", mode="md")

    tgb.text("{image_description}", mode="md")

stylekit = {"color_primary": "#FF69B4", "color-secondary": "#EE82EE"}


if __name__ == "__main__":
    url = ""
    file_address = ""
    image_description = "---"

    # Load the system prompt from the
    system_prompt = load_system_prompt("../system_prompt.txt")

    gui = Gui(chat_page)
    gui.run(
        title="Chat",
        dark_mode=False,
        stylekit=stylekit,
        use_reloader=True,
    )
