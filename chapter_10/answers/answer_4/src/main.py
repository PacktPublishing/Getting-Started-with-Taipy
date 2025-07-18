import taipy as tp
from algorithms.chat_algos_history import init_history
from algorithms.read_prompt import read_prompt
from configuration.config import conversation_scenario
from langchain_mistralai.chat_models import ChatMistralAI
from pages.analytics import analytics_page
from pages.chat_page import *
from pages.chat_page import chat_page
from taipy import Orchestrator  # ## For Answer 4
from taipy.gui import Gui
from taipy.gui import builder as tgb


def on_init(state):
    update_chat_partial(state)
    state.list_history = init_history("./history")
    if len(tp.get_scenarios()) == 0:
        state.selected_scenario = tp.create_scenario(
            conversation_scenario
        )  # create a dummy Scenario is no Scenario exists yet
    else:
        state.selected_scenario = tp.get_scenarios()[0]


with tgb.Page() as root:
    tgb.text("# **AI Transit Assistant**", mode="md")
    tgb.html("hr")
    tgb.navbar()

pages = {"/": root, "chat_page": chat_page, "analytics": analytics_page}


stylekit = {"color_primary": "#FF69B4", "color-secondary": "#EE82EE"}


if __name__ == "__main__":
    Orchestrator().run()  ### For Answer 4
    # Initialize chat model
    chat_name = "mistral-small"
    temperature = 0.6

    system_prompt = read_prompt("./prompts/system_prompt.txt", type="system")

    message_history = [system_prompt]
    chat_bot = ChatMistralAI(model=chat_name, temperature=temperature)

    # Predefined Prompts
    user_prompt_1 = read_prompt("./prompts/user_prompt_1.txt", type="human").content
    user_prompt_2 = read_prompt("./prompts/user_prompt_2.txt", type="human").content
    user_prompt_3 = read_prompt("./prompts/user_prompt_3.txt", type="human").content

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

    # Variables for history management
    open_pane = False
    list_history = []
    selected_history = None
    history_file_name = None

    #### Answer 4 ####
    selected_scenario = None

    gui = Gui(pages=pages, css_file="./css/main.css")
    chat_partial = gui.add_partial(page="")
    gui.run(
        title="The TransiBot",
        favicon="./img/chat_favicon.ico",
        dark_mode=False,
        stylekit=stylekit,
        use_reloader=True,
    )
