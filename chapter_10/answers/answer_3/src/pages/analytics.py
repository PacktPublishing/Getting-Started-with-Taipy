import json
import os
from typing import Any, Optional

import pandas as pd
import taipy.gui.builder as tgb


def parse_file_summary(file_path: str) -> Optional[dict]:
    """Extracts relevant metadata from the first and last line of an NDJSON file."""
    first_line = None
    last_line = None

    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if not line.strip():
                continue
            if i == 0:
                first_line = line
            last_line = line

    if not first_line or not last_line:
        return None

    try:
        # First line - general metadata
        first_data = json.loads(first_line)
        metadata = first_data.get("metadata", {})
        sender = metadata.get("sender")
        bot_name = metadata.get("bot_name")
        temperature = float(metadata.get("temperature", 0.0))
        date = metadata.get("date")

        # Last line - usage metadata
        last_data = json.loads(last_line)
        response_meta = last_data.get("response_metadata", {})
        usage = last_data.get("usage_metadata", {})

        return {
            "bot_name": bot_name,
            "temperature": temperature,
            "date": date,
            "model": response_meta.get("model_name"),
            "finish_reason": response_meta.get("finish_reason"),
            "total_tokens": response_meta.get("token_usage", {}).get("total_tokens"),
            "input_tokens": usage.get("input_tokens"),
            "output_tokens": usage.get("output_tokens"),
        }

    except json.JSONDecodeError:
        return None


def group_by_tokens(df):
    return df.groupby(["input_tokens", "output_tokens", "total_tokens"]).sum()


def load_history_to_dataframe(history_dir: str) -> pd.DataFrame:
    """Parses all NDJSON files in the given directory and returns a cleaned DataFrame."""
    records = []
    for filename in os.listdir(history_dir):
        if filename.endswith(".ndjson"):
            path = os.path.join(history_dir, filename)
            record = parse_file_summary(path)
            if record:
                records.append(record)
    df_records = pd.DataFrame(records)
    df_records["index"] = df_records.index
    return df_records


def refresh_data(state):
    state.df_history = load_history_to_dataframe("./history")


layout = {"barmode": "stack"}

with tgb.Page() as analytics_page:
    with tgb.layout("5 1"):
        tgb.text("## Analytics", mode="md", class_name="color-primary")
        tgb.button(label="refresh", on_action=refresh_data)

    with tgb.layout("1 1 1"):
        tgb.chart(
            "{df_history}",
            type="bar",
            x="model",
            y__1="input_tokens",
            y__2="output_tokens",
            layout=layout,
        )
        tgb.chart(
            "{df_history}",
            type="bar",
            x="index",
            y__1="input_tokens",
            y__2="output_tokens",
            layout=layout,
        )
        tgb.chart(
            "{df_history}",
            type="scatter",
            mode="markers",
            x="date",
            y__1="input_tokens",
            y__2="output_tokens",
            layout=layout,
        )
    tgb.table("{df_history}")
