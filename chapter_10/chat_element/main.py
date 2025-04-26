import re

from taipy.gui import Gui
from taipy.gui import builder as tgb
from taipy.gui import notify


def detect_and_redact_pii(text, replace_chars=True):
    """
    Detects and optionally redacts Personally Identifiable Information (PII) in a given text.

    PII (Personally Identifiable Information) includes:
    - Email addresses
    - Phone numbers (US format)
    - Names (simple title-case names or with common titles like Mr./Dr.)
    - Physical addresses (basic street address patterns)

    Args:
        text (str): The input text to scan for PII.
        replace_chars (bool, optional): If True (default), PII will be redacted by replacing
            matching characters with asterisks (*****). If False, the original text is returned.

    Returns:
        tuple:
            - redacted_text (str): The text with PII redacted if replace_chars is True,
              otherwise the original text.
            - has_pii (bool): True if any PII was found, False otherwise.
            - pii_counts (dict): A dictionary with the count of detected PII types, e.g.
              {'email': 1, 'phone': 2, 'name': 0, 'address': 1}
    """

    pii_patterns = {
        "email": r"\b[\w.-]+?@\w+?\.\w+?\b",
        "phone": r"\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b",
        "name": r"\b(?:Mr\.|Ms\.|Mrs\.|Dr\.)\s[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\b",
        "address": r"\d{1,5}\s\w+(?:\s\w+){0,3}\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b",
    }

    pii_counts = {key: 0 for key in pii_patterns}
    redacted_text = text

    for pii_type, pattern in pii_patterns.items():
        matches = list(re.finditer(pattern, text))
        pii_counts[pii_type] = len(matches)

        if replace_chars and matches:
            for match in matches:
                redacted = "*" * len(match.group())
                redacted_text = redacted_text.replace(match.group(), redacted)

    has_pii = any(count > 0 for count in pii_counts.values())
    return redacted_text, has_pii, pii_counts


def respond(state, message):
    pii_answer = detect_and_redact_pii(message)
    if pii_answer[1]:
        notify(state, "w", "Your message contains PIIs")
    response = f"""This is an anonymized version:
*****

{pii_answer[0]}
"""
    return response


def chat(state, var_name: str, payload: dict):
    messages = state.messages
    # Retrieve the callback parameters
    (_, _, user_message, sender_id) = payload.get("args", [])

    # Add the input content as a sent message
    messages.append((f"{len(messages)}", user_message, sender_id))

    try:
        result_message = respond(state, user_message)
    except Exception:
        result_message = "There was a problem!"
    messages.append((f"{len(messages)}", result_message, users[1]))
    state.messages = messages


with tgb.Page() as chat_page:
    tgb.text("# PII Analyzer", mode="md")
    tgb.html("hr")
    tgb.chat(
        messages="{messages}",
        users="{users}",
        show_sender=True,
        sender_id="{users[0]}",
        on_action=chat,
        mode="markdown",
    )

if __name__ == "__main__":
    users = ["User", "Bot"]

    messages = []
    gui = Gui(chat_page)
    gui.run(title="Simple Chat", dark_mode=False, use_reloader=True)
