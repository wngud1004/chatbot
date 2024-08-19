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

openai_api_key = st.secrets["openai_api_key"]
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

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    custom_prompt = "당신은 주어진 데이터를 바탕으로 유용하고 도움이되는 정확한 답변을 제공하는 유용한 어시스턴트입니다."
    base_data = '''
    {
        "개설학과":"컴퓨터공학과",
        "개설과목":[
            {
                "교과목명": "컴퓨터시스템구조",
                "교과구분": "전필",
                "교과번호": "561099",
                "학점": {
                    "학점": 3,
                    "강의": 6,
                    "실습": 0
                },
                "수업장소": "온라인",
                "수강대상": "2학년",
                "선행학습_및_선수과목_요건": "컴퓨터시스템기초실습, 논리회로및실습",
                "수업의_개요와_유용성": "컴퓨터의 구조와 동작에 대한 전문적인 이론과 사례연구 강의 실시 / 운영체제, 프로그래밍 언어론 등의 컴퓨터 주요 교과목들에 대한 연관 이해 / 컴퓨터의 기본적인 동작 원리와 심화적인 설계 요소들에 대한 이해 능력의 배양 / 컴퓨터 시스템의 분석과 선택에 대한 안목의 증대",
                "전공역량_및_수업목표": {
                    "주역량": {
                        "임베디드시스템개발": "70% - CPU의 구조와 동작 원리에 대한 이해 능력 향상 / 마이크로프로그래밍, 시스템 프로그래밍 능력 개발을 통한 임베디드 시스템 운용 능력 향상"
                    },
                    "부역량": {
                        "웹·앱프로그래밍 ": "30% - CPU 구조 기반의 시스템 소프트웨어 개발 능력 향상 / 프로그래밍 언어와 CPU와의 관계에 대한 이해도 향상"
                    }
                }
            },
            {
                "교과목명": "컴퓨터그래픽스",
                "교과구분": "전선",
                "교과번호": "562054",
                "학점": {
                    "학점": 3,
                    "강의": 6,
                    "실습": 0
                },
                "수업장소": "공다B 401 - 정보보안,e-biz실습실 ",
                "수강대상": "2학년",
                "선행학습_및_선수과목_요건": "컴퓨터 사용 능력, 2D 이미지 편집,  3D 모델링",
                "수업의_개요와_유용성": "이 과목은 게임 엔진 중심적인 컴퓨터 그래픽스를 다룬다. 여기에는 게임 엔진의 그래픽 렌더링 파이프라인에 대한 이해, 3D 오브젝트의 구조와 표면의 색상을 다루는 방법, 장면을 표현하고 연출하는 방법, 시각 효과(VFX), 포스트 프로세싱, 사용자의 가상현실 경험 등이 포함되나 이에 국한하지는 않는다. 수강생은 학기말까지 개별 또는 팀 프로젝트를 수행하여 게임 엔진 중심적 컴퓨터 그래픽스 결과물을 산출해야 한다. 이 수업에서 사용하는 주요 SW는 Unity, Blender, Photoshop 등이며 이외에 수업 진행을 위해 필요한 SW를 추가적으로 사용할 수 있다. 수강생은 이 과목을 통해 컴퓨터 그래픽스의 구현 원리, 게임 엔진에서의 시각적 표현 방법, 사용자 중심적인 장면 연출을 학습할 수 있다",
                "전공역량_및_수업목표": {
                    "주역량": {
                        "콘텐츠설계및응용개발": "70% - 게임 엔진 중심적 컴퓨터 그래픽스에 대한 이해와 수월성을 토대로 가상현실에 대한 사용자 경험을 증진할 수 있는 콘텐츠 제작 역량을 키운다."
                    },
                    "부역량": {
                        "웹·앱프로그래밍": "30% - 게임 엔진 및 컴퓨터 그래픽스의 특장점을 부각할 수 있는 최소한의 프로그래밍 역량을 키운다"
                    }
                }
            },
            {
                "교과목명": "자료구조",
                "교과구분": "전선",
                "교과번호": "561103",
                "학점": {
                    "학점": 3,
                    "강의": 4,
                    "실습": 4
                },
                "수업장소": "공다B 410 - 프로그램실습실, 공다A 411- 강의실",
                "수강대상": "2학년",
                "선행학습_및_선수과목_요건": "객체지향프로그래밍",
                "수업의_개요와_유용성": "컴퓨터에서 사용되는 데이터의 기본적인 구조와 이를 처리하는 여러 방법들을 연구한다. 즉 배열, 레코드, 스택, 큐, 리스트, 그래프, 트리 등의 처리 기법을 연구하며, 특히 멀티미디어 데이터의 기본적인 구조 및 이를 처리하는 여러 방법 등을 학습한다.",
                "전공역량_및_수업목표": {
                    "주역량": {
                        "정보구축및응용개발": "70% - 정보구축및응용개발 능력 상향"
                    },
                    "부역량": {
                        "웹·앱프로그래밍 ": "30% - 웹·앱프로그래밍 이해도 향상"
                    }
                }
            },
            {
                "교과목명": "시스템프로그래밍",
                "교과구분": "전선",
                "교과번호": "562005",
                "학점": {
                    "학점": 3,
                    "강의": 4,
                    "실습": 4
                },
                "수업장소": "공다B 410 - 프로그램실습실, 공다B 401- 정보보안,e-biz실습실",
                "수강대상": "2학년",
                "선행학습_및_선수과목_요건": "자바프로그래밍, c, c++, 기초 컴퓨터 시스템, 기초 컴퓨터 구조",
                "수업의_개요와_유용성": "시스템 프로그래밍 수업에서는 인텔 및 AMD 프로세서를 위한 어셈블리 언어 프로그래밍 구조에 대해서 배운다. 본 수업은 어셈블리 언어 프로그래밍, 기초 컴퓨터 시스템, 기초 컴퓨터 구조 등에 대해서 자세히 배우는 수업이다. 또한 컴퓨터 구조, 운영체제, 컴파일러 작성 등에 대한 주제를 포함하고 있다. 어셈블리언어를 배움으로써 프로세서의 내부 구조와 전반적인 컴퓨터 구조를 알 수 있도록 한다.",
                "전공역량_및_수업목표": {
                    "주역량": {
                        "임베디드시스템개발": "70% - 시스템 프로그래밍을 익혀서 입베디드 시스템 개발 능령을 함양"
                    },
                    "부역량": {
                        "정보구축및응용개발": "30% - 시스템 프로그래밍을 활용한 다양한 응용 개발 능력 함양"
                    }
                }
            },
            {
                "교과목명": "파일처리론 ",
                "교과구분": "전선",
                "교과번호": "564016",
                "학점": {
                    "학점": 3,
                    "강의": 6,
                    "실습": 0
                },
                "수업장소": "공다A 411 - 강의실",
                "수강대상": "2학년",
                "선행학습_및_선수과목_요건": "자료구조, 알고리즘",
                "수업의_개요와_유용성": "본 교과목에서는 파일 시스템의 물리적/논리적 구조를 이해하고 시스템 성능 최적화를 위한 기본지식을 학습한다. 파일을 구성하는 하드웨어적 요소와 저장 장치의 구조, 여기에 탑재되는 자료형의 종류, 각 자료형에 대한 검색 및 저장기법 등을 익힘으로써, 자료 처리 시에 필요한 파일 관리에 대하여 이해한다. 또한 입출력 성능과 관련된 인덱싱 기법 및 구조를 이해하고 이를 프로그램 해 봄으로써 실무적 능력도 학습한다.",
                "전공역량_및_수업목표": {
                    "주역량": {
                        "정보구축및응용개발 ": "70% - 컴퓨터 기반의 자료처리 시스템의 핵심적인 파일의 기본 개념과 파일 시스템, 인덱스 구조 및 파일 구성 기법과 데이터베이스와의 관계 등을 학습하고, 이를 바탕으로 다차원 공간 파일, 멀티미디어 데이터 표현을 위한 고급 파일 처리 기법 등을 학습한다."
                    },
                    "부역량": {
                        "임베디드시스템개발": "30% - 컴퓨터 기반의 자료처리 시스템의 핵심적인 개념과 파일 구성 기법 등을 이해하고, 이를 바탕으로 고급 파일 처리 기법 등을 학습한다."
                    }
                }
            },
            {
                "교과목명": "스크립트프로그래밍",
                "교과구분": "전선",
                "교과번호": "565025",
                "학점": {
                    "학점": 3,
                    "강의": 4,
                    "실습": 4
                },
                "수업장소": "공다A 410 -MacOS실습실",
                "수강대상": "2학년",
                "선행학습_및_선수과목_요건": "프론트엔드웹디자인",
                "수업의_개요와_유용성": "본 강좌에서는 프론트엔드 웹 개발 프레임워크인 리액트 라이브러리를 중점적으로 학습한다. 리액트 앱 개발 및 실행 환경인 Node.js를 학습을 통해 개발 환경을 설정하고 리액트 앱/웹 개발을 위한 핵심 요소(JSX, 컴포넌트, SCSS, Hooks 등)들을 학습한다. 이를 통해 SPA(Single Page Applicarion), 네이티브앱 등을 구현하는 역량을 기를 수 있다.",
                "전공역량_및_수업목표": {
                    "주역량": {
                        "웹·앱프로그래밍": "70% - 리액트를 활용하여 다양한 데이터를 처리하는 웹서비스를 구현할 수 있다"
                    },
                    "부역량": {
                        "정보구축및응용개발": "30% - 데이터베이스와 연계하여 데이터를 관리하는 웹서비스를 구현할 수 있다"
                    }
                }
            }
        ]
    }
    '''
    custom_prompt += f" 여기 사전 정보가 있습니다: {base_data}"

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
                {"role": "system", "content": custom_prompt},  # 시스템 메시지로 프롬프트 엔지니어링 적용
                *[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
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
        documents = []
        field_numbers = 0

        for doc in docs:
            doc_data = doc.to_dict()
            documents.append(doc_data)
            field_numbers = max(doc['id'] for doc in documents)


        # 가장 높은 숫자를 찾아 다음 필드 이름 생성
        if field_numbers != 0:
            id = field_numbers + 1
        else:
            id = 1  # 숫자 필드가 없는 경우 1로 시작

        # Firestore에 데이터 작성
        doc_ref = db.collection('chatbot').document(str(id))
        doc_ref.set({
            'id': id,
            'answer': prompt,
            'response': response
        })

