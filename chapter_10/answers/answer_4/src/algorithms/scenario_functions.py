import datetime as dt
import json
from pathlib import Path
from typing import Any

import pandas as pd
from algorithms.read_prompt import read_prompt
from langchain_core.messages import HumanMessage
from langchain_mistralai.chat_models import ChatMistralAI

######## Functions for Answer 4 ########


def create_file_path(file_name: str, folder: str = "./history") -> str:
    """Creates the full path to a file within a given folder, using pathlib."""
    return f"{folder}/{file_name}.ndjson"


def load_conversation(file_name: str) -> dict[str, Any]:
    """Loads an NDJSON conversation file into a structured dictionary."""
    file_path = create_file_path(file_name)
    conversation = []
    metadata = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            try:
                entry = json.loads(line)
                if i == 0:
                    metadata = entry.get("metadata", {})
                else:
                    conversation.append(entry)
            except json.JSONDecodeError:
                continue

    return {"metadata": metadata, "conversation": conversation}


def extract_key_parameters(data: dict[str, Any]) -> dict[str, Any]:
    """Extracts key analytic parameters from a loaded conversation."""
    convo = data.get("conversation", [])
    last_ai = next((msg for msg in reversed(convo) if msg.get("type") == "ai"), {})

    response_meta = last_ai.get("response_metadata", {})

    key_parameters = {
        "model": response_meta.get("model_name"),
        "prompt_tokens": response_meta.get("token_usage", {}).get("prompt_tokens"),
        "completion_tokens": response_meta.get("token_usage", {}).get(
            "completion_tokens"
        ),
        "total_tokens": response_meta.get("token_usage", {}).get("total_tokens"),
        "temperature": float(data.get("metadata", {}).get("temperature", 0.0)),
    }
    print(key_parameters)
    return pd.DataFrame([key_parameters])


def build_prompt_from_conversation(data: dict[str, Any]) -> str:
    """
    Formats a structured conversation dictionary into a prompt string,
    excluding system messages.
    """
    messages = []

    for msg in data.get("conversation", []):
        msg_type = msg.get("type")
        content = msg.get("content", "").strip()

        if not content:
            continue

        if msg_type == "human":
            messages.append(f"user: {content}")
        elif msg_type == "ai":
            messages.append(f"bot: {content}")
        # system messages are deliberately excluded

    conversation_str = "\n".join(messages)
    prompt = f"""Summarize the following conversation:\n\n{conversation_str}"""
    return prompt


def ask_for_summary(
    question,
    summarizer_model="mistral-small",
    temperature=0.6,
    system_prompt_address="./prompts/system_prompt_summary.txt",
):
    system_prompt = read_prompt(system_prompt_address, "system")
    question_prompt = HumanMessage(question)
    summarize_list = [system_prompt, question_prompt]

    ai_summarizer = ChatMistralAI(model=summarizer_model, temperature=temperature)
    response = ai_summarizer.invoke(summarize_list)

    return response.content
