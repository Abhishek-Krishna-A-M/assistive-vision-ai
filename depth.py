import torch
import numpy as np
import cv2
from transformers import AutoImageProcessor, AutoModelForDepthEstimation
from PIL import Image
import config

class DepthEstimator:
    def __init__(self, model_name=config.DEPTH_MODEL_NAME):
        self.processor = AutoImageProcessor.from_pretrained(model_name)
        self.model = AutoModelForDepthEstimation.from_pretrained(model_name).to(config.DEVICE)

    def estimate(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_frame)
        
        inputs = self.processor(images=pil_img, return_tensors="pt").to(config.DEVICE)
        with torch.no_grad():
            outputs = self.model(**inputs)
            predicted_depth = outputs.predicted_depth

        # Resize prediction back to original frame dimensions
        prediction = torch.nn.functional.interpolate(
            predicted_depth.unsqueeze(1),
            size=pil_img.size[::-1],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

        depth_map = prediction.cpu().numpy()
        # Relative depth normalization (0 to 1)
        depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min() + 1e-8)
        return depth_map
