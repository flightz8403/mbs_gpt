import streamlit as st
import openai
import requests
import json
import toml

st.title('MBS GPT')

# secrets = toml.load(".streamlit/secrets.toml")

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

url_params = st.query_params
if 'lang' not in st.query_params:
    lang = 'en'
else:
    lang = st.query_params["lang"]

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
            st.markdown(
                "很乐意为您说明有关于MBS模拟经营相关的问题，不过可能因为不了解您的问题，或是资料库没有准确的答案，或是AI技术的限制，我的回答请当作是参考，最好和您的同侪或是老师再次确认，感谢您的体谅。欢迎使用 MBS GPT！")
        elif lang == "zh_tw":
            st.markdown(
                "很樂意為您說明有關於MBS模擬經營相關的問題，不過可能因為不瞭解您的問題，或是資料庫沒有準確的答案，或是AI技術的限制，我的回答請當作是參考，最好和您的同儕或是老師再次確認，感謝您的體諒。歡迎使用 MBS GPT！")
        elif lang == "en":
            st.markdown("I am happy to explain to you the questions related to MBS business simulation, but it maybe because I do not understand your question, or the database does not have an accurate answer, or the limitation of AI technology, please take my answer as a reference, it is best to confirm with your peers or teachers, thank you for your understanding. Welcome to MBS GPT!")
        elif lang == "jp":
            st.markdown("MBS経営シミュレーションに関するご質問については、喜んでご説明させていただきますが、ご質問の内容が理解できなかったり、データベースに正確な回答がなかったり、AI技術の限界があったりするため、私の回答を参考にしていただければと思います。 、同僚や先生に確認するのが最善です、ご理解いただきありがとうございます。 MBS GPTへようこそ！")
        elif lang == "th":
            st.markdown("ฉันยินดีที่จะอธิบายให้คุณทราบเกี่ยวกับคำถามที่เกี่ยวข้องกับการจำลองธุรกิจ MBS แต่อาจเป็นเพราะฉันไม่เข้าใจคำถามของคุณ หรือฐานข้อมูลไม่มีคำตอบที่ถูกต้อง หรือข้อจำกัดของเทคโนโลยี AI โปรดใช้คำตอบของฉันเป็นข้อมูลอ้างอิง เป็นการดีที่สุดที่จะยืนยันกับเพื่อนหรือครูของคุณ ขอขอบคุณสำหรับความเข้าใจของคุณ ยินดีต้อนรับสู่ MBS GPT!")
        elif lang == "id":
            st.markdown("Saya dengan senang hati menjelaskan kepada Anda pertanyaan terkait simulasi bisnis MBS, tetapi mungkin karena saya tidak memahami pertanyaan Anda, atau database tidak memiliki jawaban yang akurat, atau keterbatasan teknologi AI, harap ambil jawaban saya sebagai referensi. , sebaiknya konfirmasi dengan teman atau guru, terima kasih atas pengertiannya. Selamat datang di MBS GPT!")

# chatpdf_api_key = st.secrets["CHATPDF_API_KEY"]
# chatpdf_source_id = st.secrets["CHATPDF_SOURCE_ID"]

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

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",  # Specify the model for chat applications
            temperature = 0.7,
            messages=[
                {"role": "system", "content": "You are a teaching assistant specializing in business management. Answer in as much detail as possible."},
                {"role": "user", "content": prompt},
            ],
        )
        
        # Extracting the text from the last response in the chat
        if response.choices:
        
            result = response.choices[0].message.content.strip()

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(result)
            # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": result})

            # Add feedback loop
            # col1, col2, col3, col4, col5, col6, c7, c8 = st.columns(8)    
            # with col2: 
            #    st.button(':thumbsdown:', on_click=thumbsdown, args=[prompt, result])
            # with col3:
            #    st.button(':thumbsup:', on_click=thumbsup, args=[prompt, result])

        else:

            result = "No response from the model."

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(result)
            # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": result})

    except Exception as e:
        print(f"An error occurred: {str(e)}") 
    
        '''
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
        '''

    
