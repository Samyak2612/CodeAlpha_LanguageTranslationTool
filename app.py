import streamlit as st
import pandas as pd
import pyperclip

from config import APP_NAME, LANGUAGES
from translator import translate_text
from history import save_history, load_history
from tts import generate_audio
from utils import show_success, show_error, character_count

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

.main-title{
    font-size:48px;
    font-weight:bold;
    text-align:center;
    color:#0E76FD;
}

.sub-title{
    text-align:center;
    color:gray;
    font-size:18px;
    margin-bottom:25px;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:30px;
}

div[data-testid="stButton"] button{
    width:100%;
    border-radius:12px;
    height:48px;
    font-size:17px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------

if "text" not in st.session_state:
    st.session_state.text = ""

if "translated" not in st.session_state:
    st.session_state.translated = ""

if "source" not in st.session_state:
    st.session_state.source = "English"

if "target" not in st.session_state:
    st.session_state.target = "Hindi"

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("🌍 AI Translator")

st.sidebar.success("⚡ Fast • Accurate • AI Powered")

st.sidebar.markdown("---")

st.sidebar.write("### Features")

st.sidebar.write("✅ 100+ Languages")

st.sidebar.write("✅ Auto Detect")

st.sidebar.write("✅ Text To Speech")

st.sidebar.write("✅ Download Translation")

st.sidebar.write("✅ Translation History")

st.sidebar.markdown("---")

st.sidebar.info("Developer\n\nSamyak Jain")

# -----------------------------
# TITLE
# -----------------------------

st.markdown(
    "<div class='main-title'>🌍 AI Language Translation Tool</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>Translate text instantly into multiple languages.</div>",
    unsafe_allow_html=True
)

# -----------------------------
# LANGUAGE SELECTION
# -----------------------------

col1,col2 = st.columns(2)

language_names = list(LANGUAGES.keys())

with col1:

    source = st.selectbox(
        "Source Language",
        language_names,
        index=language_names.index(st.session_state.source)
    )

with col2:

    target_languages = language_names[1:]

    target = st.selectbox(
        "Target Language",
        target_languages,
        index=target_languages.index(st.session_state.target)
    )

# -----------------------------
# TEXT INPUT
# -----------------------------

text = st.text_area(
    "Enter Text",
    value=st.session_state.text,
    height=170,
    placeholder="Type your text here..."
)

st.caption(f"Characters : {character_count(text)}")

# -----------------------------
# BUTTONS
# -----------------------------

c1,c2,c3 = st.columns(3)

translate_btn = c1.button("🌍 Translate")

swap_btn = c2.button("🔄 Swap")

clear_btn = c3.button("🗑 Clear")

# -----------------------------
# TRANSLATE
# -----------------------------

if translate_btn:

    if text.strip() == "":
        show_error("Please enter some text.")

    else:

        try:

            translated = translate_text(
                text,
                LANGUAGES[source],
                LANGUAGES[target]
            )

            st.session_state.text = text
            st.session_state.translated = translated
            st.session_state.source = source
            st.session_state.target = target

            save_history(
                source,
                target,
                text,
                translated
            )

            show_success("Translation Successful ✅")

        except Exception as e:

            show_error(str(e))

# -----------------------------
# SWAP
# -----------------------------

if swap_btn:

    if st.session_state.source != "Auto Detect":

        temp_language = st.session_state.source
        st.session_state.source = st.session_state.target
        st.session_state.target = temp_language

    temp_text = st.session_state.text
    st.session_state.text = st.session_state.translated
    st.session_state.translated = temp_text

    st.rerun()

# -----------------------------
# CLEAR
# -----------------------------

if clear_btn:

    st.session_state.text = ""
    st.session_state.translated = ""
    st.session_state.source = "English"
    st.session_state.target = "Hindi"

    st.rerun()

# -----------------------------
# OUTPUT
# -----------------------------

if st.session_state.translated != "":

    st.markdown("---")

    st.subheader("🌍 Translated Text")

    st.text_area(
        "Result",
        value=st.session_state.translated,
        height=170
    )

# -----------------------------
# HISTORY
# -----------------------------

st.markdown("---")

st.subheader("📜 Translation History")

history_df = load_history()

if len(history_df) > 0:

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No history available yet.")

# -----------------------------
# EXTRA FEATURES
# -----------------------------

if st.session_state.translated != "":

    st.markdown("### ⚡ Quick Actions")

    b1, b2, b3 = st.columns(3)

    # Copy Button
    if b1.button("📋 Copy Translation"):

        try:
            pyperclip.copy(st.session_state.translated)
            st.success("Copied to clipboard!")
        except Exception:
            st.warning("Clipboard access isn't available on this system.")

    # Download Button
    b2.download_button(
        "📥 Download TXT",
        data=st.session_state.translated,
        file_name="translation.txt",
        mime="text/plain"
    )

    # Text-to-Speech
    if b3.button("🔊 Play Audio"):

        try:

            lang_code = LANGUAGES[st.session_state.target]

            # gTTS doesn't support "auto"
            if lang_code == "auto":
                lang_code = "en"

            audio_path = generate_audio(
                st.session_state.translated,
                lang_code
            )

            with open(audio_path, "rb") as audio:
                st.audio(audio.read())

        except Exception as e:
            st.error(f"Audio Error: {e}")

# -----------------------------
# STATISTICS
# -----------------------------

st.markdown("---")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Characters",
    character_count(st.session_state.text)
)

c2.metric(
    "Translated Characters",
    character_count(st.session_state.translated)
)

history_df = load_history()

c3.metric(
    "Translations",
    len(history_df)
)

# -----------------------------
# FOOTER
# -----------------------------

st.markdown("---")

st.markdown(
"""
<div class='footer'>

### 🌍 AI Language Translation Tool

Developed by <b>Samyak Jain</b>

Built with ❤️ using Python & Streamlit

</div>
""",
unsafe_allow_html=True
)