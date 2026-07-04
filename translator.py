from deep_translator import GoogleTranslator


def translate_text(text, source, target):
    """
    Translate text using Google Translator.
    """

    translator = GoogleTranslator(
        source=source,
        target=target
    )

    return translator.translate(text)