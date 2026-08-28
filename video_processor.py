import cv2
from detector import ObjectDetector
from depth import DepthEstimator
from ocr import TextReader
from navigation import NavigationEngine
from speech import SpeechEngine
from utils import annotate_frame

class PipelineProcessor:
    def __init__(self, run_ocr=True):
        print("Initializing AI Pipeline Components...")
        self.detector = ObjectDetector()
        self.depth_estimator = DepthEstimator()
        self.ocr_reader = TextReader() if run_ocr else None
        self.nav_engine = NavigationEngine()
        self.speech = SpeechEngine()

    def process_video(self, source_path=0, output_path=None, frame_skip=3):
        cap = cv2.VideoCapture(source_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30

        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            detections = self.detector.detect(frame)
            depth_map = self.depth_estimator.estimate(frame)
            
            # OCR runs periodically to save processing bandwidth
            ocr_results = []
            if self.ocr_reader and (frame_count % frame_skip == 0):
                ocr_results = self.ocr_reader.read_text(frame)

            instructions = self.nav_engine.evaluate(detections, depth_map, ocr_results, width)

            if instructions:
                self.speech.speak(instructions[0])

            annotated = annotate_frame(frame, detections, ocr_results, instructions)

            if writer:
                writer.write(annotated)
                
            # Press 'q' to stop early during live video tests
            cv2.imshow("Assistive Vision Pipeline", annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        if writer:
            writer.release()
        cv2.destroyAllWindows()
        print("Processing finished cleanly.")
