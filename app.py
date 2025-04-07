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

# セッションで入力を保持
if "url_input" not in st.session_state:
    st.session_state.url_input = ""

st.title("📋 YouTube文字起こしコピーツール")
st.write("YouTubeのURLを入力すると、文字起こしが表示されます。末尾に『上記の文章を要約してください。』が付きます。")

# 入力欄 + クリアボタン（横並び）
col1, col2 = st.columns([5, 1])
with col1:
    st.text_input("🔗 YouTubeのURLを入力してください", value=st.session_state.url_input, key="url_input")
with col2:
    if st.button("✖️"):
        st.session_state.url_input = ""
        st.experimental_rerun()

# 実行ボタン（下に配置）
if st.button("文字起こしを取得する") and st.session_state.url_input:
    video_id = extract_video_id(st.session_state.url_input)
    if video_id:
        try:
            transcript = get_transcript(video_id)
            final_text = transcript + "\n\n上記の文章を要約してください。"
            st.success("以下の文字をそのままコピーして、ChatGPTに貼ってください👇")
            st.code(final_text, language='text')

            components.html(
                """
                <script>
                const textarea = window.parent.document.querySelector('textarea');
                if (textarea) {
                    textarea.focus();
                    textarea.select();
                }
                </script>
                """,
                height=0,
            )

        except Exception as e:
            st.error(f"文字起こしの取得中にエラーが発生しました：{e}")
    else:
        st.error("正しいYouTubeのURLを入力してください")
