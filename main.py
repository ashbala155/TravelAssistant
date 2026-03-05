import streamlit as st
import PyPDF2
import io
from openai import OpenAI
from dotenv import load_dotenv
import base64

load_dotenv()

st.set_page_config(page_title="AI Travel Itinerary Assistant", page_icon="✈️", layout="centered")

# Background image
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://images.unsplash.com/photo-1500964757637-c85e8a162699?q=80&w=1803&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
  background-size: cover;
}
</style>
""", unsafe_allow_html=True)

st.title("🏄🏻🏖️🧳 AI Travel Itinerary Assistant")
st.markdown("Ask about any travel destination - we'll find the best suggestions for you!")

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# -----------------------------
# User inputs
# -----------------------------
uploaded_file = st.file_uploader("Upload a travel guide if you have any (optional) PDF/TXT", type=["pdf", "txt"])
query = st.text_input("Enter your travel question (e.g., Plan a 4-day itinerary for Rome / Best places to visit Paris):")
analyze = st.button("Ask AI")

# -----------------------------
# PDF/TXT text extraction
# -----------------------------
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

# -----------------------------
# AI request
# -----------------------------
if analyze and query:
    try:
        context = extract_text_from_file(uploaded_file) if uploaded_file else "give appropriate travel recommendations"

        prompt = f"""
You are a helpful travel assistant.
Use the following travel guide context to answer the question.

Context:
{context}

Question:
{query}

Please provide your analysis in a clear, structured format with specific recommendations.
Answer:
"""

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert travel itinerary planner with years of experience as a travel agent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        ai_text = response.choices[0].message.content
        st.markdown("### 🗺 AI-Generated Travel Itinerary")
        st.markdown(ai_text.replace("\n", "  \n"))

        # Download as TXT
        b64 = base64.b64encode(ai_text.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="itinerary.txt">💾 Download Itinerary as TXT</a>'
        st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
