import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Model Paths & Setup
YOLO_MODEL_PATH = "yolov8s.pt"
DEPTH_MODEL_NAME = "LiheYoung/depth-anything-small-hf"

# Detection & OCR Thresholds
YOLO_CONF_THRESH = 0.25
OCR_CONF_THRESH = 0.45

# Depth Map Levels (0-255 scale)
VERY_CLOSE_THRESH = 179
CLOSE_THRESH = 115

# Time threshold (in seconds) to prevent redundant speech spam
COOLDOWN_SECONDS = 3.0
