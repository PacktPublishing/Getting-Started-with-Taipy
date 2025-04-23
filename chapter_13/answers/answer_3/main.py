import asyncio
import json

import pandas as pd
import taipy.gui.builder as tgb
from taipy import Gui
from taipy.gui import Gui, invoke_long_callback
from websockets import connect


async def wikipedia_edits(data_queue):
    async with connect("wss://wikimon.hatnote.com/") as ws:
        while True:
            msg = await ws.recv()
            edit = json.loads(msg)
            dict_msg = {
                "action": edit.get("action"),
                "user": edit.get("user"),
                "page": edit.get("page_title"),
                "change_size": edit.get("change_size"),
                "is_new": edit.get("is_new"),
                "is_minor": edit.get("is_minor"),
                "is_new": edit.get("is_new"),
            }
            await data_queue.put(dict_msg)


async def process_data(data_queue):
    global df_wikipedia_edits
    while True:
        dict_msg = await data_queue.get()
        df_wikipedia_edits = pd.concat(
            [df_wikipedia_edits, pd.DataFrame([dict_msg])], ignore_index=True
        )
        print(df_wikipedia_edits)

        data_queue.task_done()


async def listen_wiki():
    data_queue = asyncio.Queue()
    producer = asyncio.create_task(wikipedia_edits(data_queue))
    consumer = asyncio.create_task(process_data(data_queue))

    await asyncio.gather(producer, consumer)


def start_listening():
    asyncio.run(listen_wiki())


def update_wikipedia_df(state):
    print("updating UI")
    global df_wikipedia_edits

    state.df_wiki = df_wikipedia_edits


def on_init(state):
    invoke_long_callback(state, start_listening, [], update_wikipedia_df, [], 1000)


with tgb.Page() as wikipedia_page:
    tgb.text("# **Wikipedia** Data", mode="md")

    tgb.table("{df_wiki}", rebuild=True)


if __name__ == "__main__":
    df_wikipedia_edits = pd.DataFrame()
    df_wiki = pd.DataFrame(
        columns=[
            "action",
            "user",
            "page",
            "change_size",
            "is_new",
            "is_minor",
            "is_new",
        ]
    )

    gui = Gui(page=wikipedia_page)
    gui.run(title="Wikipedia Page", dark_mode=False, use_reloader=True)
