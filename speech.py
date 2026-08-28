import pyttsx3

class SpeechEngine:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 165)
        except Exception:
            self.engine = None  # Handles headless Google Colab environments gracefully

    def speak(self, text):
        if not text:
            return
        print(f"🔊 AUDIO OUT: '{text}'")
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                pass
