from gtts import gTTS
import tempfile

SUPPORTED_LANGS = {
    "en","hi","fr","de","es","it","pt",
    "ru","ja","ko","ar","tr","nl","ur",
    "ta","te","bn","gu","pa","ml","kn"
}

def generate_audio(text, language):

    if language not in SUPPORTED_LANGS:
        language = "en"

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    gTTS(
        text=text,
        lang=language,
        slow=False
    ).save(temp.name)

    return temp.name