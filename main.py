import streamlit as st
import json
import os
import time
import base64
import folium
from streamlit_folium import st_folium
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai
from groq import Groq

API_KEY = "Gemini API Key"
GROQ_KEY = "GROQ API Key "

st.set_page_config(page_title="Kibou Assistant 🇯🇵", layout="wide", page_icon="🇯🇵")

# إعداد مكتبة Google Generative AI
genai.configure(api_key=API_KEY)

if "groq_client" not in st.session_state:
    st.session_state.groq_client = Groq(api_key=GROQ_KEY)

if 'page' not in st.session_state:
    st.session_state.page = "Home"

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

def render_subject_page(subject_name, folder_name, years):
    with st.sidebar:
        st.title(f" {subject_name} Controls")
        year_choice = st.selectbox(f"Select Year:", ["Select"] + years, key=f"{subject_name}_year")
        
        if year_choice != "Select":
            pdf_path = os.path.join(folder_name, f"{year_choice}.pdf")
            
            if os.path.exists(pdf_path):
                file_key = f"ref_{subject_name}_{year_choice}"
                
                if file_key not in st.session_state:
                    with st.spinner("Uploading PDF to Gemini..."):
                        try:
                            # الطريقة الصحيحة لرفع الملفات في الإصدار الجديد
                            g_file = genai.upload_file(path=pdf_path)
                            while g_file.state.name == "PROCESSING":
                                time.sleep(2)
                                g_file = genai.get_file(g_file.name)
                            st.session_state[file_key] = g_file
                            st.success("✅ File Ready!")
                        except Exception as e:
                            st.error(f"Upload Error: {e}")

                q_desc = st.text_input("Question (e.g. Q1):", key=f"{subject_name}_q")
                
                if st.button("🚀 Solve", use_container_width=True):
                    with st.spinner("Thinking..."):
                        try:
                            model = genai.GenerativeModel("gemini-flash-latest")
                            prompt = f"Expert MEXT {subject_name} Tutor. Solve {q_desc} from the PDF step-by-step."
                            response = model.generate_content([st.session_state[file_key], prompt])
                            st.session_state[f"res_{subject_name}"] = response.text
                        except Exception as e:
                            st.error(f"AI Error: {e}")

                if f"res_{subject_name}" in st.session_state:
                    st.markdown("---")
                    st.markdown("### 📝 AI Result:")
                    st.info(st.session_state[f"res_{subject_name}"])

                st.write("---")
                user_ask = st.text_area("💬 Ask AI anything else:", key=f"{subject_name}_ask")
                if st.button("Send Query", use_container_width=True):
                    if user_ask:
                        with st.spinner("Thinking..."):
                            try:
                                model = genai.GenerativeModel("gemini-flash-latest")
                                extra_res = model.generate_content([st.session_state[file_key], user_ask])
                                st.session_state[f"extra_{subject_name}"] = extra_res.text
                            except Exception as e:
                                st.error(f"Error: {e}")
                
                if f"extra_{subject_name}" in st.session_state:
                    st.markdown("### 💡 AI Response:")
                    st.write(st.session_state[f"extra_{subject_name}"])
            else:
                st.error(f"File not found: {pdf_path}")

        st.write("---")
        if st.button("🔙 Back to Home"): go_to("Home")

    if year_choice != "Select" and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="900px" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

# --- 3. LOGIC FOR NAVIGATION ---
if st.session_state.page == "Home":
    st.title("🇯🇵 Kibou Assistant (希望)")
    st.subheader("Welcome back, Abdulrahman Salah!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧮 Math Pathway", use_container_width=True): go_to("Math_Page")
        if st.button("🧪 Chemistry Pathway", use_container_width=True): go_to("Chemistry_Page")
        if st.button("🎙️ AI Interviewer", use_container_width=True): go_to("Interview")
    with col2:
        if st.button("⚡ Physics Pathway", use_container_width=True): go_to("Physics_Page")
        if st.button("📖 English Pathway", use_container_width=True): go_to("English_Page")

# --- 4. SUBJECT PAGES ---
elif st.session_state.page == "Math_Page":
    render_subject_page("Math", "Math", ["2014", "2015", "2016", "2017", "2018", "2019"])
elif st.session_state.page == "Physics_Page":
    render_subject_page("Physics", "Physics", ["2014", "2015", "2016", "2017", "2018", "2019"])
elif st.session_state.page == "Chemistry_Page":
    render_subject_page("Chemistry", "Chemistry", ["2014", "2015", "2016", "2017", "2018", "2019"])
elif st.session_state.page == "English_Page":
    render_subject_page("English", "English", ["2017", "2018"])

# --- 5. INTERVIEW PAGE ---
elif st.session_state.page == "Interview":
    st.title("🎓 MEXT Interviewer")
    
    if "messages" not in st.session_state: st.session_state.messages = []
    if "chat_session" not in st.session_state: st.session_state.chat_session = None

    with st.sidebar:
        st.header("Settings")
        user_files = st.file_uploader("Upload CV / Study Plan", accept_multiple_files=True, type=['pdf', 'docx', 'jpg', 'png'])
        if st.button("Reset Interview"):
            st.session_state.messages = []
            st.session_state.chat_session = None
            if "files_ready" in st.session_state: del st.session_state.files_ready
            st.rerun()
        if st.button("🔙 Back"): go_to("Home")

    if user_files and "files_ready" not in st.session_state:
        with st.spinner("Processing documents..."):
            refs = []
            for uf in user_files:
                temp_name = f"temp_{uf.name}"
                with open(temp_name, "wb") as f: f.write(uf.getbuffer())
                g = genai.upload_file(path=temp_name)
                while g.state.name == "PROCESSING": time.sleep(1); g = genai.get_file(g.name)
                refs.append(g)
                os.remove(temp_name)
            st.session_state.gemini_docs = refs
            st.session_state.files_ready = True
            
            sys_instr = "You are a MEXT expert. 1. Ask tough questions. 2. Give Feedback. 3. Be concise."
            model = genai.GenerativeModel("gemini-flash-latest", system_instruction=sys_instr)
            st.session_state.chat_session = model.start_chat(history=[])
            
            r = st.session_state.chat_session.send_message(["Start interview and analyze these documents:", *st.session_state.gemini_docs])
            st.session_state.messages.append({"role": "interviewer", "content": r.text})

    if st.session_state.get("files_ready"):
        for msg in st.session_state.messages:
            if msg["role"] == "interviewer": st.info(f"🎙️ **Interviewer:** {msg['content']}")
            else: st.success(f"👤 **You:** {msg['content']}")
        
        audio_data = mic_recorder(start_prompt="Speak Answer 🎤", stop_prompt="Send 📤", key=f"mic_{len(st.session_state.messages)}")
        if audio_data and audio_data.get('bytes'):
            trans = st.session_state.groq_client.audio.transcriptions.create(file=("a.wav", audio_data['bytes']), model="whisper-large-v3")
            if trans.text:
                st.session_state.messages.append({"role": "user", "content": trans.text})
                resp = st.session_state.chat_session.send_message(trans.text)
                st.session_state.messages.append({"role": "interviewer", "content": resp.text})
                st.rerun()

