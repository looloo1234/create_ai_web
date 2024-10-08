import streamlit as st
from openai import OpenAI
import base64
import requests

# 사이드바에서 API 키 입력 받기
st.sidebar.title("API 설정")
api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")

# API 키가 입력되었는지 확인
if api_key:
    # OpenAI 클라이애티어트 초기화
    client = OpenAI(api_key=api_key)

    # Streamlit 페이지 제목 설정
    st.title("DALL-E 3 이미지 생성 및 분석기")

    # 이미지 파일 업로드 받기
    uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # 업로드된 이미지 출력
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # 업로드된 이미지 base64 인코딩
        base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')

        # OpenAI API를 사용하여 이미지 분석
        analysis_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "이미지를 자세히 분석해주세요."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        # 결과 출력
        st.subheader("이미지 분석 결과")
        st.write(analysis_response.choices[0].message.content)

        # 텍스트에서 다시 이미지 생성하기
        new_prompt = analysis_response.choices[0].message.content
        if st.button("분석 결과로 이미지 생성"):
            new_image_response = client.images.generate(
                model="dall-e-3",
                prompt=new_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            new_image_url = new_image_response.data[0].url
            st.image(new_image_url, caption=f"Generated Image from Analysis: {new_prompt}")

    # 사용자 입력 받기
    object_name = st.text_input("학생이 좋아하는 물건을 입력하세요", "a teddy bear")
    prompt = f"{object_name} with arms and legs"

    # 버튼을 클릭했을 때 이미지 생성
    if st.button("이미지 생성"):
        # OpenAI API를 사용하여 이미지 생성
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # 생성된 이미지 URL 가져오기
        image_url = response.data[0].url

        # 이미지 출력
        st.image(image_url, caption=f"Generated Image: {prompt}")
else:
    st.warning("API 키를 사이드바에 입력하세요.")