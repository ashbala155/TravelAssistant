import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

st.set_page_config(page_title="AI Travel Itinerary Assistant", page_icon="✈️", layout="centered")

st.title("✈️ AI Travel Itinerary Assistant")
st.markdown("Ask about any travel destination - we'll find the best suggestions for you!")


#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

st.subheader("❓ Ask Your Question")
uploaded_file = st.file_uploader("Upload a travel guide if you have any (optional) PDF/TXT", type=["pdf", "txt"])
query = st.text_input("Enter your travel question (e.g., Best places to visit in Paris):")
analyze = st.button("Ask")

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

if analyze and query:
    try:
        context = extract_text_from_file(uploaded_file)

        prompt = f"""You are a helpful travel assistant.
        Use the following travel guide context to answer the question.
        If the answer is not found, say you don't know — don’t make it up.

        Context:
        {context if context else 'give appropriate travel recommendations'}

        Question:
        {query}

        
        Please provide your analysis in a clear, structured format with specific recommendations.
        Answer:"""
        
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
        st.markdown("### Analysis Results")
        st.markdown(response.choices[0].message.content)
    
    except Exception as e:
        st.error(f"An error occured: {str(e)}")

        

        
    