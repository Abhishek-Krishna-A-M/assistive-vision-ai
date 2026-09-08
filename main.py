from video_processor import PipelineProcessor

if __name__ == "__main__":
    # Pass 0 for live webcam, or "sample.mp4" for test video file
    processor = PipelineProcessor(run_ocr=True)
    #processor.process_video(source_path=0)
    processor.process_video(source_path="sample.mp4", output_path="output_demo.mp4")
