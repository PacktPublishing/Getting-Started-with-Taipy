import json
import os

from algorithms.create_history_scenario import create_history_scenario
from langchain_core.messages import HumanMessage


def save_history(msg, file_path: str):
    """Append a full Langchain message as a JSON line (NDJSON)."""
    if not hasattr(msg, "type"):
        raise ValueError(f"Unsupported message type: {type(msg)}")

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(msg.dict()) + "\n")


def init_history(directory):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".ndjson"):
            files.append(os.path.splitext(filename)[0])
            create_history_scenario(filename)  ##### Add this for Answer 4
    return files


def talk_to_bot(input_message, history, chat, json_history_path):
    human_message = HumanMessage(content=input_message)

    save_history(human_message, json_history_path)
    history.append(human_message)
    response = chat.invoke(history)
    history.append(response)
    save_history(response, json_history_path)
    return response, history
