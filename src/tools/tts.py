import os
from elevenlabs.client import ElevenLabs
from gtts import gTTS

from src.config.env import ELEVENLABS_API_KEY
from langchain_core.tools import tool

@tool
def text_to_speech(text: str, filename: str = "output.wav", engine: str = "elevenlabs") -> str:
    """
    Converts text to speech using the specified TTS engine and saves it to a file.

    Args:
        text (str): The text to convert to speech.
        filename (str): The name of the file to save the audio to. Defaults to "output.wav".
        engine (str): The TTS engine to use. Can be "elevenlabs" or "gtts". Defaults to "elevenlabs".

    Returns:
        str: A message indicating the file was saved successfully.
    """
    if engine == "elevenlabs":
        return text_to_speech_elevenlabs(text, filename)
    elif engine == "gtts":
        return text_to_speech_gtts(text, filename)
    else:
        return "Invalid TTS engine specified. Please use 'elevenlabs' or 'gtts'."

def text_to_speech_elevenlabs(text: str, filename: str) -> str:
    """
    Converts text to speech using ElevenLabs API and saves it to a file.
    """
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=text,
        voice="Bella",
        model="eleven_multilingual_v2"
    )
    with open(filename, "wb") as f:
        f.write(audio)
    return f"Audio saved to {filename}"

def text_to_speech_gtts(text: str, filename: str) -> str:
    """
    Converts text to speech using gTTS and saves it to a file.
    """
    tts = gTTS(text)
    tts.save(filename)
    return f"Audio saved to {filename}"
