import datetime
from threading import Thread

import requests
from taipy.gui import Gui
from taipy.gui import builder as tgb
from taipy.gui import get_state_id, invoke_callback

html_text = ""
time_with_threads = 0
time_without_threads = 0

urls = {
    "wikipedia": "https://www.wikipedia.org",
    "python.org": "https://www.python.org",
    "arxiv": "https://arxiv.org/",
    "wikimedia": "https://commons.wikimedia.org/wiki/",
    "archive.org": "https://web.archive.org/",
}
websites = ["wikipedia", "python.org", "arxiv", "wikimedia", "archive.org"]
selected_websites = websites


def fetch_url(url):
    try:
        response = requests.get(url)
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")


def update_html_text(state, update_html, start):
    state.html_text += update_html
    end = datetime.datetime.now() - start
    state.time_with_threads = end.total_seconds()


def fetch_text(state_id, url, start):
    update_html = fetch_url(url)
    invoke_callback(gui, state_id, update_html_text, [update_html, start])


def scrape_websites_threads(state):
    start = datetime.datetime.now()
    state.html_text = ""
    for website in state.websites:
        url = urls[website]
        print(url)

        thread = Thread(target=fetch_text, args=[get_state_id(state), url, start])
        thread.start()


def scrape_websites_no_threads(state):
    start = datetime.datetime.now()
    state.html_text = ""

    for website in state.websites:
        url = urls[website]
        update_html = fetch_url(url)
        state.html_text += update_html

    end = datetime.datetime.now() - start
    state.time_without_threads = end.total_seconds()


with tgb.Page() as scrape_page:
    tgb.text("# Scrape several websites", mode="md")

    tgb.selector("{selected_websites}", lov=websites, multiple=True, dropdown=True)

    with tgb.layout("1 1"):
        tgb.button("Scrape with threads", on_action=scrape_websites_threads)
        tgb.button("Scrape without threads", on_action=scrape_websites_no_threads)

        tgb.text("## Time using Threads: {time_with_threads}", mode="md")
        tgb.text("## Time without using Threads: {time_without_threads}", mode="md")

    tgb.text("{html_text}")

if __name__ == "__main__":
    gui = Gui(page=scrape_page)
    gui.run(dark_mode=False)  # , use_reloader=True)
