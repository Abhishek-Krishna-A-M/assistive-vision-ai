from video_processor import PipelineProcessor

if __name__ == "__main__":
    # Pass 0 for live webcam, or a video file path for test video
    processor = PipelineProcessor(run_ocr=True)
    #processor.process_video(source_path=0)
    processor.process_video(source_path=0)
