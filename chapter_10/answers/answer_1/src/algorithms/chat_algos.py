from langchain_core.messages import HumanMessage
from langchain_mistralai.chat_models import ChatMistralAI


def talk_to_bot(input_message, history, chat):
    history.append(HumanMessage(content=input_message))
    response = chat.invoke(history)
    history.append(response)
    return response, history
