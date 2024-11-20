import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def main():
    st.title("Gemini PDF 분석기")
    
    # API 키 입력
    api_key = st.text_input("Google API 키를 입력하세요:", type="password")
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            # PDF 파일 업로드
            uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=['pdf'])
            
            if uploaded_file is not None:
                # PDF에서 텍스트 추출
                text_content = extract_text_from_pdf(uploaded_file)
                
                # 사용자 질문 입력
                user_question = st.text_input("PDF에 대해 질문하세요:")
                
                if user_question:
                    # 프롬프트 구성
                    prompt = f"다음 텍스트를 바탕으로 질문에 답변해주세요.\n\n텍스트: {text_content}\n\n질문: {user_question}"
                    
                    try:
                        response = model.generate_content(prompt)
                        st.write("답변:")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"응답 생성 중 오류가 발생했습니다: {str(e)}")
                        
        except Exception as e:
            st.error(f"API 키 설정 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()
