import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re
import streamlit.components.v1 as components

st.set_page_config(page_title="YouTube文字起こしコピーツール", layout="centered")

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ja', 'en'])
    return " ".join([entry['text'] for entry in transcript])

# セッション状態を使って入力内容を管理
if "url_input" not in st.session_state:
    st.session_state.url_input = ""

st.title("📋 YouTube文字起こしコピーツール")
st.write("YouTubeのURLを入力すると、文字起こしが表示されます。末尾に『上記の文章を要約してください。』が付きます。")

# 入力欄とクリアボタンを横並びに表示
col1, col2 = st.columns([4, 1])
with col1:
    url = st.text_input("🔗 YouTubeのURLを入力してください", value=st.session_state.url_input, key="url_input")

with col2:
    if st.button("クリア"):
        st.session_state.url_
