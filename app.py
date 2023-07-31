import streamlit as st
import requests
import json

st.title('MBS GPT')

url_params = st.experimental_get_query_params()
lang = url_params["lang"][0]

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def thumbsup(prompt, result):
    st.session_state.clicked = True
    feedback_url = 'http://mbs.top-boss.com:1269/gpt/feedback'

    params = json.dumps({
        "data": {
            "prompt": prompt,
            "result": result,
            "type": 'mbs',
            "feedback": 1
        }
    })
    response = requests.request("POST", feedback_url, data=params)

def thumbsdown(prompt, result):
    st.session_state.clicked = True
    feedback_url = 'http://mbs.top-boss.com:1269/gpt/feedback'

    params = json.dumps({
        "data": {
            "prompt": prompt,
            "result": result,
            "type": 'mbs',
            "feedback": -1
        }
    })
    response = requests.request("POST", feedback_url, data=params)
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message("assistant"):
        if lang == "zh_cn":
            st.markdown("欢迎使用 MBS GPT！ 请询问任何有关MBS模拟系统的问题！")
        elif lang == "zh_tw":
            st.markdown("歡迎使用 MBS GPT！ 請詢問任何有關MBS模擬系統的問題！")
        elif lang == "en":
            st.markdown("Welcome to MBS GPT! Please ask any question you have regarding MBS simulation system!")
        elif lang == "jp":
            st.markdown("MBS GPTへようこそ！ MBSシミュレーションシステムに関するご質問は何でもご質問ください！")
        elif lang == "th":
            st.markdown("ยินดีต้อนรับสู่ MBS GPT! โปรดถามคำถามใด ๆ ที่คุณมีเกี่ยวกับระบบจำลอง MBS!")
        elif lang == "id":
            st.markdown("Selamat datang di MBS GPT! Silakan ajukan pertanyaan apa pun yang Anda miliki tentang sistem simulasi MBS!")

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

    # Add feedback loop
    col1, col2, col3, col4, col5, col6, c7, c8 = st.columns(8)    
    with col2: 
        st.button(':thumbsdown:', on_click=thumbsdown, args=[prompt, result])
    with col3:
        st.button(':thumbsup:', on_click=thumbsup, args=[prompt, result])

    
