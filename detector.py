from ultralytics import YOLO
import config

class ObjectDetector:
    def __init__(self, model_path=config.YOLO_MODEL_PATH):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame, verbose=False, conf=config.YOLO_CONF_THRESH)[0]
        detections = []
        for box in results.boxes:
            cls_id = int(box.cls[0].item())
            name = self.model.names[cls_id]
            conf = float(box.conf[0].item())
            xyxy = box.xyxy[0].cpu().numpy().tolist()
            
            detections.append({
                "name": name,
                "confidence": conf,
                "box": [int(v) for v in xyxy]
            })
        return detections
