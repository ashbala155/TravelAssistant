import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

st.set_page_config(page_title="AI Travel Itinerary Assistant", page_icon="✈️", layout="centered")

page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://plus.unsplash.com/premium_photo-1681487892519-d197931571be?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
  background-size: cover;
}
</style>
"""

st.markdown(page_element, unsafe_allow_html=True)

st.title("🏄🏻🏖️🧳 AI Travel Itinerary Assistant")
st.markdown("Ask about any travel destination - we'll find the best suggestions for you!")


#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

st.subheader("❓Ask Your Travel Question or Give Us a Destination")
uploaded_file = st.file_uploader("Upload a travel guide if you have any (optional) PDF/TXT", type=["pdf", "txt"])
query = st.text_input("Enter your travel question (e.g., Plan a 4 day itinerary for Rome/ Best places to visit in Paris):")
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
        if uploaded_file:
         context = extract_text_from_file(uploaded_file)
        else:
            context = "give appropriate travel recommendations"

        prompt = f"""You are a helpful travel assistant.
        Use the following travel guide context to answer the question.

        Context:
        {context}

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
        st.markdown(response.choices[0].message.content)
    
    except Exception as e:
        st.error(f"An error occured: {str(e)}")

        

        
    
