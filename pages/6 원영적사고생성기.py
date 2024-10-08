import streamlit as st
import google.generativeai as genai

# 사이드바에서 API 키 입력 받기
st.sidebar.title("API 설정")
api_key = st.sidebar.text_input("Google Gemini API 키를 입력하세요", type="password")

# API 키가 입력되었는지 확인
if api_key:
    # API 키 설정
    genai.configure(api_key=api_key)

    # Streamlit 페이지 제목 설정
    st.title("원영적 사고 생성기")

    # 생성 설정
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # 모델 초기화
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # 사용자 입력 받기
    user_input = st.text_area("당신의 기분을 입력하세요", 
                              "예: 나는 오늘 다리를 다쳐서 학교 못나가서 슬퍼.")

    if st.button("원영적 사고 생성"):
        # 인공지능 모델을 사용하여 상장 생성
        response = model.generate_content([
            "부정적인 상황을 긍정적으로 생각할 수 있도록 중학생,학생들에게 얘기해주고자 합니다. 예를 들면 갑자기 비가 오는 상황. 원영적 사고는 갑자기 비가 와서 추워 🥺☁️☁️ 그런데 운치있는 빗소리를 들을 수 있으니까 완전 럭키비키잖아💛✨라고 얘기하는거야. 입력의 내용을 참고하여 재치있는 사고 과정과 문구를 생성해주세요. 그리고 럭키비키잖아💛✨는 끝에 꼭 들어가야해",
            f"input: {user_input}",
        ])

        # 결과 출력
        st.subheader("생성된 원영적 사고")
        st.write(response.text)
else:
    st.warning("API 키를 사이드바에 입력하세요.")
