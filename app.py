import streamlit as st
import json
import google.genai as genai

# Page config
st.set_page_config(page_title="Mental Health AI", page_icon="🧠", layout="centered")

# API setup
client = genai.Client(api_key="PASTE_YOUR_API_KEY_HERE")

# Title
st.title("🧠 Mental Health Support AI")
st.markdown("An AI system that analyzes emotional text and provides empathetic support responses.")
st.divider()

# Analysis function
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

st.subheader("How are you feeling?")

# 1. Initialize session state for the text input if it doesn't exist
if 'user_query' not in st.session_state:
    st.session_state.user_query = ""

# 2. Define functions to update the session state for each button
def set_sample_text(text):
    st.session_state.user_query = text

# Sample buttons
st.markdown("**Try a sample:**")
col1, col2, col3 = st.columns(3)

# Use on_click to update the state before the app re-runs
col1.button("😔 Depression", on_click=set_sample_text, args=("I've been feeling really down for weeks. I can't get out of bed and lost interest in everything.",))
col2.button("😰 Anxiety", on_click=set_sample_text, args=("My heart keeps racing. I feel like something terrible is about to happen all the time.",))
col3.button("😰 Stress", on_click=set_sample_text, args=("Work has been overwhelming. I can't sleep and feel exhausted but can't stop thinking.",))

# 3. Bind the text_area to the session state using the 'value' parameter
user_input = st.text_area("Share what's on your mind...", value=st.session_state.user_query, height=120, key="main_input")

# Analyze button
if st.button("Analyze", type="primary") and user_input:
    # Your existing analysis logic below...
    with st.spinner("Analyzing..."):
        try:
            # Note: Ensure analyze_text is the function that orchestrates the LangGraph 
            # or model calls described in your project files[cite: 166, 174, 184].
            result = analyze_text(user_input) 
            
            st.divider()
            st.subheader("Analysis Results")
            
            # (Rest of your UI code remains the same)
            col1, col2 = st.columns(2)
            col1.metric("Primary Concern", result.get("primary_concern", "unclear").title())
            col2.metric("Severity Level", result.get("severity_level", "unclear").title())
            
            if result.get("safety_concerns"):
                # Project safety logic: prioritize providing the 988 lifeline[cite: 76, 117].
                st.error("⚠️ Safety concern detected. Please contact the 988 Suicide & Crisis Lifeline by calling or texting 988.")

            st.info(f"**Analysis:** {result.get('analysis_summary', '')}")
            st.subheader("Support Response")
            st.success(result.get("support_response", ""))

        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.divider()
st.caption("This tool is for informational purposes only and is not a substitute for professional mental health care.")
