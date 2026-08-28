import cv2
import numpy as np

def annotate_frame(frame, detections, ocr_results, instructions):
    annotated = frame.copy()
    
    # Render Detection Bounding Boxes
    for obj in detections:
        xmin, ymin, xmax, ymax = obj["box"]
        cv2.rectangle(annotated, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        label = f"{obj['name']} {obj['confidence']:.2f}"
        cv2.putText(annotated, label, (xmin, max(15, ymin - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Render OCR Bounding Boxes
    for ocr in ocr_results:
        pts = np.array(ocr["box"], np.int32).reshape((-1, 1, 2))
        cv2.polylines(annotated, [pts], True, (255, 0, 0), 2)
        cv2.putText(annotated, ocr["text"], (pts[0][0][0], max(15, pts[0][0][1] - 5)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Overlay Active Voice Instruction Bar
    if instructions:
        cv2.rectangle(annotated, (0, 0), (annotated.shape[1], 45), (0, 0, 0), -1)
        cv2.putText(annotated, f"AUDIO: {instructions[0]}", (15, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    return annotated
