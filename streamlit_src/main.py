import streamlit as st
from llm_utils import get_llm_response
from utils import trigger_scraping, save_chat_to_django, get_all_chats, get_chat_by_id, load_chat_history

st.title("Real Estate Chatbot")
st.sidebar.title("Chat Settings")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = "New Chat"


def chat_sidebar():
    all_chats = get_all_chats()
    print(all_chats)
    chat_options = [f"Chat {chat['id']}" for chat in all_chats] if all_chats else []

    selected_chat = st.sidebar.selectbox(
        "Select an existing chat:",
        options=["New Chat"] + chat_options,
        index=(["New Chat"] + chat_options).index(st.session_state.selected_chat)
        if st.session_state.selected_chat in ["New Chat"] + chat_options
        else 0
    )

    if selected_chat != st.session_state.selected_chat:
        st.session_state.selected_chat = selected_chat

        if selected_chat != "New Chat":
            selected_chat_id = int(selected_chat.split()[1])
            st.session_state.chat_id = selected_chat_id
            st.session_state.chat_history = load_chat_history(selected_chat_id)

        else:
            st.session_state.chat_id = None
            st.session_state.chat_history = []

chat_sidebar()

st.header("Chat with our AI-powered assistant")
chat_container = st.container()
user_input = st.text_input("Your message:", "")

if st.button("Send"):
    if user_input.strip():

        st.session_state.chat_history.append({"sender": "user", "message": user_input})
        chat_id = save_chat_to_django(st.session_state.chat_id, "user", user_input)

        if chat_id and not st.session_state.chat_id:
            st.session_state.chat_id = chat_id
            st.session_state.selected_chat = f"Chat {chat_id}"

        bot_response = get_llm_response(user_input, st.session_state.chat_history)
        st.session_state.chat_history.append({"sender": "bot", "message": bot_response})
        save_chat_to_django(st.session_state.chat_id, "bot", bot_response)

        if not bot_response:
            st.error("Failed to get a response from the AI assistant.")


with chat_container:
    for message in st.session_state.chat_history:
        if message["sender"] == "user":
            st.markdown(f"**You:** {message['message']}")
        elif message["sender"] == "bot":
            st.markdown(f"**Bot:** {message['message']}")


st.sidebar.header("Scraping Controls")
all_pages = st.sidebar.checkbox("Scrape all pages", value=False)


if st.sidebar.button("Start Scraping"):
    success, message = trigger_scraping(all_pages)

    if success:
        st.success(message)
    else:
        st.error(message)

