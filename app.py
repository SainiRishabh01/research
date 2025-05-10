import streamlit as st
import os
import pandas as pd
import plotly.express as px
import requests

from utils import (
    search_research_papers,
    summarize_paper,
    comparative_analysis,
    text_to_speech
)

# Page config
st.set_page_config(page_title="Research Paper Summarizer", page_icon="📚", layout="wide")

# --- Title ---
st.markdown("<h1 style='text-align: center;'>📚 Research Paper Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Get the latest research papers, analysis, and listen to summaries</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Input Section ---
with st.container():
    st.markdown("### 🔍 Enter Research Topic")
    topic = st.text_input("Topic", placeholder="e.g., Artificial Intelligence, Quantum Computing")

# --- Fetch Papers ---
if st.button("🚀 Fetch Papers"):
    if not topic.strip():
        st.error("⚠️ Please enter a valid topic.")
    else:
        with st.spinner(f"Fetching papers for '{topic}'..."):
            papers = search_research_papers(topic)

        if not papers:
            st.warning("❌ No papers found.")
        else:
            # --- Display Paper Cards ---
            st.markdown("### 📝 Research Papers")
            for paper in papers:
                st.markdown(f"**🔹 [{paper['title']}]({paper['link']})**")
                st.write(paper["summary"])
                st.markdown(f"`Topics:` {', '.join(paper['topics'])} | `Sentiment:` {paper['sentiment']}")
                st.markdown("---")

            # --- Sentiment Analysis Visualization ---
            result = comparative_analysis(papers)
            sentiment_data = result.get("Sentiment Distribution", {})

            if sentiment_data:
                st.markdown("### 📊 Sentiment Distribution")
                df = pd.DataFrame(list(sentiment_data.items()), columns=["Sentiment", "Count"])

                col1, col2 = st.columns(2)
                with col1:
                    pie = px.pie(df, names="Sentiment", values="Count", title="Sentiment Distribution")
                    st.plotly_chart(pie, use_container_width=True)
                with col2:
                    bar = px.bar(df, x="Sentiment", y="Count", title="Sentiment Count", color="Sentiment")
                    st.plotly_chart(bar, use_container_width=True)

            # --- Audio Summary + Translated Text ---
            st.markdown("### 🎧 Audio Summary")
            summary_text = " ".join([paper['summary'] for paper in papers])

            if summary_text.strip():
                try:
                    audio_file, translated_text = text_to_speech(summary_text)
                    if os.path.exists(audio_file):
                        st.audio(audio_file, format="audio/mp3")
                        with open(audio_file, "rb") as f:
                            st.download_button("⬇️ Download Audio", f, "summary.mp3", "audio/mp3")
                except Exception as e:
                    st.error(f"Error generating audio: {str(e)}")
            else:
                st.warning("⚠️ No valid summaries found for TTS.")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center;'>Made by <b>Your Name</b> • "
    "<a href='https://github.com/yourgithubprofile' target='_blank'>GitHub</a></p>",
    unsafe_allow_html=True
)
