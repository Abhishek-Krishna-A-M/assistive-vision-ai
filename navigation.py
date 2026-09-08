import time
import numpy as np
import config

class NavigationEngine:
    def __init__(self):
        self.last_announced = {}

    def _get_spatial_zone(self, box, img_width):
        xmin, _, xmax, _ = box
        center_x = (xmin + xmax) / 2.0
        third = img_width / 3.0
        
        if center_x < third:
            return "on your left"
        elif center_x > 2 * third:
            return "on your right"
        else:
            return "ahead"

    def _get_depth_level(self, depth_map, box):
        xmin, ymin, xmax, ymax = box
        h, w = depth_map.shape
        xmin, ymin = max(0, int(xmin)), max(0, int(ymin))
        xmax, ymax = min(w, int(xmax)), min(h, int(ymax))

        if len(depth_map.shape) == 3:
            depth_map = depth_map[:, :, 0] if depth_map.shape[2] == 1 else depth_map.mean(axis=2)
        depth_map = depth_map.astype(np.float64)

        box_depth = depth_map[ymin:ymax, xmin:xmax]
        if box_depth.size == 0:
            return "Far"

        mean_depth = float(np.mean(box_depth))
        if mean_depth >= config.VERY_CLOSE_THRESH:
            return "Very Close"
        elif mean_depth >= config.CLOSE_THRESH:
            return "Close"
        return "Far"

    def evaluate(self, detections, depth_map, ocr_results, frame_width):
        current_time = time.time()
        instructions = []

        # 1. Prioritize Close/Very Close Hazards
        hazards = []
        for obj in detections:
            depth_lvl = self._get_depth_level(depth_map, obj["box"])
            pos = self._get_spatial_zone(obj["box"], frame_width)
            
            if depth_lvl in ["Very Close", "Close"]:
                hazards.append((obj["name"], depth_lvl, pos))

        # Sort so "Very Close" items trigger first
        hazards.sort(key=lambda x: 0 if x[1] == "Very Close" else 1)

        for name, depth_lvl, pos in hazards:
            key = f"{name}_{pos}"
            if key not in self.last_announced or (current_time - self.last_announced[key] > config.COOLDOWN_SECONDS):
                if depth_lvl == "Very Close" and pos == "ahead":
                    instructions.append("Obstacle very close ahead. Step aside.")
                else:
                    instructions.append(f"{name.capitalize()} {pos}.")
                self.last_announced[key] = current_time

        # 2. Text/Sign Alerts (Only if no collision risk)
        if not instructions and ocr_results:
            for ocr in ocr_results:
                text_str = ocr["text"]
                if text_str not in self.last_announced or (current_time - self.last_announced[text_str] > config.COOLDOWN_SECONDS * 2):
                    instructions.append(f"Sign reads: {text_str}")
                    self.last_announced[text_str] = current_time
                    break

        return instructions
