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
            st.markdown(prompt)

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

                # Firebase 인증서 설정 및 초기화
        cred = credentials.Certificate("auth.json")
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        else:
            print("Firebase app is already initialized.")

        # Firestore 데이터베이스 클라이언트 가져오기
        db = firestore.client()

        collection_ref = db.collection('chatbot')
        docs = collection_ref.stream()

        response_ids = []
        id = 2

        for doc in docs:
            doc_data = doc.to_dict()
            
            # 디버깅 정보를 위한 출력
            print(f"Document ID: {doc.id}, Document Data: {doc_data}")

            # 'response' 필드가 존재하는지 확인
            if 'response' in doc_data and isinstance(doc_data['response'], dict):
                response_id = doc_data['response'].get('id', None)
                
                if response_id is not None:
                    response_ids.append(response_id)
                else:
                    print(f"No 'id' found in 'response' field in document with ID: {doc.id}")
            else:
                print(f"'response' field is missing or not a dictionary in document with ID: {doc.id}")
        
        print(response_ids)
        if response is not None:
            id = max(response_ids) + 1

        # Firestore에 데이터 작성
        doc_ref = db.collection('chatbot').document('response')
        doc_ref.set({
            'id': id,
            'answer': prompt,
            'response': response
        })

