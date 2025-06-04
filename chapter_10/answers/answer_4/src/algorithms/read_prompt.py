from langchain_core.messages import HumanMessage, SystemMessage


def read_prompt(file_name, type):
    with open(file_name, "r") as prompt:
        prompt_text = prompt.read()

    if type == "system":
        message = SystemMessage(prompt_text)
    elif type == "human":
        message = HumanMessage(prompt_text)
    return message
