# 🇯🇵 Kibou Assistant (希望)

**Kibou Assistant** (Hope) is an AI-powered educational platform designed specifically for students applying for the **Japanese Government (MEXT) Scholarship**. The tool serves as an intelligent tutor for solving past papers and a rigorous interviewer to prepare candidates for the final selection stages.

## 🚀 Features

* **Subject Pathways:** Dedicated modules for **Mathematics**, **Physics**, **Chemistry**, and **English** past papers.
* **AI Tutor:** Integrates **Google Gemini Flash 1.5** to solve specific questions from PDF past papers step-by-step.
* **Live PDF Viewer:** Side-by-side view of the exam paper and the AI-generated solution.
* **AI Interviewer:** A mock interview simulator that:
    * Analyzes your uploaded CV and Study Plan.
    * Uses **Groq (Whisper-large-v3)** for high-speed voice-to-text transcription.
    * Acts as a tough MEXT expert to provide feedback and challenging questions.
* **Voice Interaction:** Practice your interview answers using voice commands, simulating a real-world interview experience.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (for a fast, interactive web interface).
* **LLM (Text/Vision):** [Google Generative AI (Gemini)](https://ai.google.dev/).
* **STT (Speech-to-Text):** [Groq API](https://groq.com/) with **Whisper-large-v3**.
* **PDF Processing:** Base64 encoding for embedded browser rendering.

---

## 📁 Project Structure

```text
kibou-assistant/
├── app.py              # Main Streamlit application code
├── Math/               # PDF past papers for Math (2014-2019)
├── Physics/            # PDF past papers for Physics (2014-2019)
├── Chemistry/          # PDF past papers for Chemistry (2014-2019)
├── English/            # PDF past papers for English
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/3bod999/Kibou-Assistant.git
   cd kibou-assistant
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **API Keys Configuration:**
   * Replace `API_KEY` with your **Google Gemini API Key**.
   * Replace `GROQ_KEY` with your **Groq API Key**.
   * *Note: For production, use `st.secrets` or environment variables.*

4. **Run the App:**
   ```bash
   streamlit run main.py
   ```

---
