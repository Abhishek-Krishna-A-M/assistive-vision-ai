from gtts import gTTS
from IPython.display import Audio, display
import os

class SpeechEngine:
    def __init__(self):
        pass

    def speak(self, text):
        if not text:
            return
        print(f"🔊 AUDIO OUT: '{text}'")
        try:
            # Generate speech audio file
            tts = gTTS(text=text, lang='en')
            audio_path = "speech.mp3"
            tts.save(audio_path)
            
            # Play through mobile browser speaker automatically
            display(Audio(audio_path, autoplay=True))
        except Exception as e:
            print(f"Audio playback error: {e}")
