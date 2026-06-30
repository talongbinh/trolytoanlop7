import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# Cấu hình trang
st.set_page_config(page_title="Trợ lý Toán lớp 7 - Thầy Bình", page_icon="🤖")
st.title("🤖 Trợ Lý Toán Lớp 7 - Thầy Long Bình")

# Nhập API Key
api_key = st.sidebar.text_input("Nhập API Key của thầy:", type="password")

# Hàm đọc PDF
def get_pdf_text(file_path):
    reader = PdfReader(file_path)
    return "\n".join([page.extract_text() for page in reader.pages])

if api_key:
    genai.configure(api_key=api_key)
    
    # Đọc nội dung PDF (Thay tên 'bai_tap.pdf' bằng đúng tên file của thầy)
    try:
        knowledge = get_pdf_text("Test.pdf") 
    except:
        knowledge = "Chưa tải file PDF lên."

    # Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Nhập tên câu cần hỏi (ví dụ: Câu 1)...")
    
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        
        prompt = f"Dựa trên đề bài này: {knowledge}. Hãy hướng dẫn học sinh giải câu hỏi: {user_input}. Nhớ làm theo đúng phong cách sư phạm thầy Long Bình đã dặn."
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.write(response.text)
        
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": response.text})
