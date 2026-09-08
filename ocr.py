import cv2
import easyocr
import config

class TextReader:
    def __init__(self, lang_list=['en']):
        self.reader = easyocr.Reader(lang_list, gpu=(config.DEVICE == "cuda"))

    def read_text(self, frame):
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.reader.readtext(rgb_frame)
        except Exception:
            return []
        detected_texts = []
        for bbox, text, conf in results:
            if conf >= config.OCR_CONF_THRESH:
                detected_texts.append({
                    "text": text.strip(),
                    "confidence": conf,
                    "box": bbox
                })
        return detected_texts
