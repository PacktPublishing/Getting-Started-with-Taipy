import datetime as dt
import json
import os
import uuid
from dataclasses import asdict, dataclass

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


@dataclass
class HistoryMetadata:
    id: int
    date: str
    time_stamp: str
    name: str
    filename: str
    sender: str
    bot_name: str


def generate_history_metadata(
    prompt: str, sender, bot_name, history_dir: str = "./history"
) -> HistoryMetadata:
    now = dt.datetime.now(dt.timezone.utc)
    current_date = now.date().isoformat()
    current_timestamp = now.isoformat()
    unique_id = uuid.uuid4().int
    name = f"{prompt.strip()[:40]}...({unique_id})"
    os.makedirs(history_dir, exist_ok=True)
    filename = f"{history_dir}/{name}.ndjson"

    metadata = HistoryMetadata(
        id=unique_id,
        date=current_date,
        time_stamp=current_timestamp,
        name=name,
        filename=filename,
        sender=sender,
        bot_name=bot_name,
    )

    # First line = metadata
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps({"metadata": asdict(metadata)}) + "\n")

    return metadata


def save_history(msg, file_path: str):
    """Append a full Langchain message as a JSON line (NDJSON)."""
    if not hasattr(msg, "type"):
        raise ValueError(f"Unsupported message type: {type(msg)}")

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(msg.dict()) + "\n")


def load_history(file_path: str):
    """Load Langchain messages from NDJSON file, skipping the metadata line."""
    msg_classes = {
        "human": HumanMessage,
        "system": SystemMessage,
        "ai": AIMessage,
    }

    messages = []
    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            data = json.loads(line.strip())
            if i == 0 and "metadata" in data:
                continue  # Skip metadata

            msg_type = data.get("type")
            cls = msg_classes.get(msg_type)
            if cls:
                messages.append(cls(**data))
            else:
                raise ValueError(f"Unsupported message type: {msg_type}")

    return messages


def get_users(file_path: str) -> tuple[str, str]:
    """Reads the metadata line of an NDJSON file and extracts sender and bot_name."""
    with open(file_path, "r", encoding="utf-8") as f:
        first_line = f.readline()
        metadata = json.loads(first_line).get("metadata", {})

    sender = metadata.get("sender", "User")
    bot_name = metadata.get("bot_name", "Bot")
    return sender, bot_name


def create_display_list(
    message_history: list, sender: str, bot_name: str
) -> list[tuple[int, str, str]]:
    """Converts a LangChain message list into a display-friendly tuple list."""
    display_list = []
    counter = 0

    for msg in message_history:
        # Skip system prompts for display
        if isinstance(msg, SystemMessage):
            continue
        if isinstance(msg, HumanMessage):
            speaker = sender
        elif isinstance(msg, AIMessage):
            speaker = bot_name
        else:
            continue

        display_list.append((counter, msg.content, speaker))
        counter += 1

    return display_list


def init_history(directory):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".ndjson"):
            files.append(os.path.splitext(filename)[0])
    return files


def read_prompt(file_name, type):
    with open(file_name, "r") as prompt:
        prompt_text = prompt.read()

    if type == "system":
        message = SystemMessage(prompt_text)
    elif type == "human":
        message = HumanMessage(prompt_text)
    return message


def talk_to_bot(input_message, history, chat, json_history_path):
    human_message = HumanMessage(content=input_message)

    save_history(human_message, json_history_path)
    history.append(human_message)
    response = chat.invoke(history)
    history.append(response)
    save_history(response, json_history_path)
    return response, history
