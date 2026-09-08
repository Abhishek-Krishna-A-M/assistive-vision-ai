import os

class SpeechEngine:
    def __init__(self):
        self.use_colab = False
        try:
            from IPython.display import Audio, display
            import IPython
            self.use_colab = True
        except ImportError:
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
            except Exception:
                self.engine = None

    def speak(self, text):
        if not text:
            return
        print(f"🔊 AUDIO OUT: '{text}'")
        try:
            if self.use_colab:
                from IPython.display import Audio, display
                from gtts import gTTS
                tts = gTTS(text=text, lang='en')
                audio_path = "speech.mp3"
                tts.save(audio_path)
                display(Audio(audio_path, autoplay=True))
            elif self.engine:
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                from gtts import gTTS
                tts = gTTS(text=text, lang='en')
                tts.save("speech.mp3")
                os.system("mpg321 speech.mp3 2>/dev/null || afplay speech.mp3 2>/dev/null || echo 'Audio saved to speech.mp3'")
        except Exception as e:
            print(f"Audio playback error: {e}")
