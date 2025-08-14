import streamlit as st
from joke_generator.generator import run_joke_workflow

st.set_page_config(page_title="Joke Content Generator", page_icon="😂", layout="centered")
st.title("😂 Joke Content Generator")
st.markdown("""
Welcome! Enter a topic and get a audience-friendly, AI-generated joke with creative key points. Perfect for a comedian or just to share a laugh!
""")

topic = st.text_input("Enter a topic for your joke:", "AI Engineer Role")

if st.button("Generate Joke"):
    if topic.strip():
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        with st.spinner("Generating joke and key points using AI workflow..."):
            result = run_joke_workflow(topic, openai_api_key)
        st.success("Joke Generated!")
        st.markdown(f"**Key Points:**\n{result['keypoints']}")
        st.markdown("---")
        st.subheader("Here's your joke:")
        st.markdown(f"> {result['joke']}")
    else:
        st.warning("Please enter a topic to generate a joke.")

st.markdown("""
---
*Built with [Streamlit](https://streamlit.io/) & [LangGraph](https://langchain-ai.github.io/langgraph/).*
""")
