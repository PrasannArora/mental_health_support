import streamlit as st
import json
import os
import google.genai as genai

st.set_page_config(page_title="Mental Health AI", page_icon="🧠", layout="centered")

client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

st.title("🧠 Mental Health Support AI")
st.markdown("An AI system that analyzes emotional text and provides empathetic support responses.")
st.divider()

# Sample buttons using session state (this is the correct Streamlit way)
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

st.subheader("How are you feeling?")

col1, col2, col3 = st.columns(3)
if col1.button("😔 Depression"):
    st.session_state.input_text = "I've been feeling really down for weeks. I can't get out of bed and lost interest in everything I used to enjoy."
if col2.button("😰 Anxiety"):
    st.session_state.input_text = "My heart keeps racing. I feel like something terrible is about to happen all the time."
if col3.button("😓 Stress"):
    st.session_state.input_text = "Work has been overwhelming. I can't sleep and feel exhausted but can't stop thinking."

user_input = st.text_area("Share what's on your mind...", 
                           value=st.session_state.input_text, 
                           height=120,
                           key="text_area")

def analyze_text(text):
    prompt = f"""Analyze this text for mental health indicators. Return ONLY valid JSON, no markdown.
Text: "{text}"
Return: {{"primary_concern":"depression|anxiety|crisis|stress|unclear","severity_level":"low|moderate|high|critical","key_themes":["theme1","theme2"],"safety_concerns":true or false,"analysis_summary":"2 sentence summary","support_response":"3-4 sentence empathetic response"}}"""
    response = client.models.generate_content(
        model="models/gemini-3.1-flash-lite-preview",
        contents=prompt
    )
    raw = response.text.replace("```json","").replace("```","").strip()
    return json.loads(raw)

if st.button("Analyze", type="primary") and user_input:
    with st.spinner("Analyzing..."):
        try:
            result = analyze_text(user_input)
            st.divider()
            st.subheader("Analysis Results")

            col1, col2 = st.columns(2)
            col1.metric("Primary Concern", result.get("primary_concern", "unclear").title())
            col2.metric("Severity Level", result.get("severity_level", "unclear").title())

            themes = result.get("key_themes", [])
            if themes:
                st.markdown("**Key themes detected:**")
                st.write(" · ".join(themes))

            if result.get("safety_concerns"):
                st.error("⚠️ Safety concern detected. Please contact the 988 Suicide & Crisis Lifeline by calling or texting 988.")

            st.info(f"**Analysis:** {result.get('analysis_summary', '')}")
            st.subheader("Support Response")
            st.success(result.get("support_response", ""))

        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.divider()
st.caption("This tool is for informational purposes only and is not a substitute for professional mental health care.")
