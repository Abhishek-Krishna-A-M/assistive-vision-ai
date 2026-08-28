import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Model Paths & Setup
YOLO_MODEL_PATH = "yolov8n.pt"
DEPTH_MODEL_NAME = "LiheYoung/depth-anything-small-hf"

# Detection & OCR Thresholds
YOLO_CONF_THRESH = 0.50
OCR_CONF_THRESH = 0.45

# Depth Map Levels (Normalized relative scale: 0.0=Far, 1.0=Very Close)
VERY_CLOSE_THRESH = 0.70
CLOSE_THRESH = 0.45

# Time threshold (in seconds) to prevent redundant speech spam
COOLDOWN_SECONDS = 3.0
