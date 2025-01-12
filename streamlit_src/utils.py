# Constants
import os
import time

import requests

from dotenv import load_dotenv

load_dotenv()

DJANGO_HOST = os.getenv("DJANGO_HOST", "django")

CHATS_URL = f"http://{DJANGO_HOST}:8000/api/chats/"
CHATS_MESSAGE_URL = f"http://{DJANGO_HOST}:8000/api/chat_messages/"
SCRAPING_URL = f"http://{DJANGO_HOST}:8000/api/scrapping/"
HOMES_URL = f"http://{DJANGO_HOST}:8000/api/homes/"
ADD_MESSAGE_URL = f"http://{DJANGO_HOST}:8000/api/add_message/"


def query_api(filters):
    try:
        print(filters)
        response = requests.get(HOMES_URL, params=filters)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        return None


def save_chat_to_django(chat_id, sender, message):
    message_payload = {"message": {"sender": sender, "message": message}}
    if chat_id:
        message_payload["chat_id"] = chat_id

    message_response = requests.post(f"{ADD_MESSAGE_URL}", json=message_payload)

    if message_response.status_code not in [200, 201]:
        return None

    created_message = message_response.json()
    print("Chat saved")
    return created_message["chat_id"]


def trigger_scraping(all_pages):
    payload = {"all_pages": all_pages}
    response = requests.post(SCRAPING_URL, json=payload)

    if response.status_code == 200:
        return True, "Scraping triggered successfully."
    else:
        return False, "Failed to trigger scraping."


def get_all_chats():
    response = requests.get(CHATS_URL)
    if response.status_code == 200:
        return response.json()

def get_chat_by_id(chat_id):
    response = requests.get(f"{CHATS_URL}{chat_id}/")
    if response.status_code == 200:
        return response.json()

def load_chat_history(selected_chat_id):
    return get_chat_by_id(selected_chat_id)["messages"]
