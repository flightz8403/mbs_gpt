import streamlit as st
import requests
import json

st.title('MBS GPT')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

chatpdf_api_key = st.secrets["CHATPDF_API_KEY"]
chatpdf_source_id = st.secrets["CHATPDF_SOURCE_ID"]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question"):
# Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    url = "https://api.chatpdf.com/v1/chats/message"

    payload = json.dumps({
        "sourceId": chatpdf_source_id,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    headers = {
        'x-api-key': chatpdf_api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    result = json.loads(response.text)['content']
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(result)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": result})

    