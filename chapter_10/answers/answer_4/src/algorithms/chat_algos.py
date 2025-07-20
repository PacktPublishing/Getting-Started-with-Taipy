import datetime as dt
import json
import os
import re
import uuid
from dataclasses import asdict, dataclass
from typing import Any

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
    temperature: float


def get_metadata(file_path: str) -> dict[str, Any]:
    """Reads the metadata line of an NDJSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        first_line = f.readline()
        return json.loads(first_line).get("metadata")


def get_users_from_metadata(metadata: dict[str, Any]) -> tuple[str, str, float]:
    """Extracts sender, bot_name, and temperature from metadata."""
    sender = metadata.get("sender")
    bot_name = metadata.get("bot_name")
    temperature = float(metadata.get("temperature", 0.0))  # Safe default
    return sender, bot_name, temperature


def get_users(file_path: str) -> tuple[str, str, float]:
    """Convenience function to get users directly from a file."""
    metadata = get_metadata(file_path)
    return get_users_from_metadata(metadata)


def sanitize_filename(prompt: str, unique_id: str) -> str:
    # Trim, take first 30 chars, replace spaces with underscores
    base = prompt.strip()[:30]
    base = base.replace(" ", "_")

    # Remove all non-alphanumeric or underscore characters
    base = re.sub(r"[^A-Za-z0-9_]", "", base)

    # Ensure it doesn't start with a digit
    if base and base[0].isdigit():
        base = f"f_{base}"

    return f"{base}_{unique_id}"


def create_metadata_object(
    prompt: str,
    sender: str,
    bot_name: str,
    temperature: float,
    history_dir: str,
) -> tuple[HistoryMetadata, str]:
    """Creates a HistoryMetadata object and corresponding filename."""
    now = dt.datetime.now(dt.timezone.utc)
    current_date = now.date().isoformat()
    current_timestamp = now.isoformat()
    unique_id = uuid.uuid4().int
    name = sanitize_filename(prompt, unique_id)

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
        temperature=temperature,
    )

    return metadata, filename


def write_metadata_to_file(metadata: HistoryMetadata, filename: str) -> None:
    """Writes the metadata as the first line of the NDJSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps({"metadata": asdict(metadata)}) + "\n")


def generate_history_metadata(
    prompt: str,
    sender: str,
    bot_name: str,
    temperature: float,
    history_dir: str = "./history",
) -> HistoryMetadata:
    """Generates and writes HistoryMetadata to an NDJSON file."""
    metadata, filename = create_metadata_object(
        prompt, sender, bot_name, temperature, history_dir
    )
    write_metadata_to_file(metadata, filename)
    return metadata


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
