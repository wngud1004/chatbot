import streamlit as st
from openai import OpenAI

import firebase_admin 
from firebase_admin import credentials
from firebase_admin import firestore

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Firebase 인증서 설정 및 초기화
    cred = credentials.Certificate("auth.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    else:
        print("Firebase app is already initialized.")

    # Firestore 데이터베이스 클라이언트 가져오기
    db = firestore.client()

    
    # 컬렉션의 모든 문서를 가져옴
    collection_ref = db.collection('chatbot')
    docs = collection_ref.stream()

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(docs[0])

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # 컬렉션의 모든 문서를 가져옴
        collection_ref = db.collection('chatbot')
        docs = collection_ref.stream()

        # 숫자로 된 필드 이름을 수집하기 위한 리스트
        field_numbers = []

        for doc in docs:
            doc_data = doc.to_dict()

            # 숫자만으로 된 필드 이름을 확인
            for key in doc_data.keys():
                try:
                    # 필드 이름이 숫자인지 확인
                    number = int(key)
                    field_numbers.append(number)
                except ValueError:
                    pass  # 필드 이름이 숫자가 아닌 경우 건너뛰기

        # 가장 높은 숫자를 찾아 다음 필드 이름 생성
        if field_numbers:
            id = max(field_numbers) + 1
        else:
            id = 1  # 숫자 필드가 없는 경우 1로 시작

        # Firestore에 데이터 작성
        doc_ref = db.collection('chatbot').document(str(id))
        doc_ref.set({
            'answer': prompt,
            'response': response
        })

