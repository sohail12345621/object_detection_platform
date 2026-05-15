import cv2
import os
from ultralytics import YOLO
from loguru import logger
import supervision as sv

def get_model(model_name: str = "yolov8n.pt"):
    """Loads a YOLOv8 model, downloading it if necessary."""
    weights_dir = "../weights"
    os.makedirs(weights_dir, exist_ok=True)
    model_path = os.path.join(weights_dir, model_name)
    
    try:
        # ultralytics will auto-download if not found locally when passed the name like 'yolov8n.pt'
        model = YOLO(model_name)
        return model
    except Exception as e:
        logger.error(f"Failed to load model {model_name}: {e}")
        raise e

def process_image(input_path: str, output_path: str, model_name: str = "yolov8n.pt", conf_threshold: float = 0.25):
    """Processes an image through YOLOv8 and saves the annotated result."""
    logger.info(f"Processing image {input_path} with {model_name}")
    model = get_model(model_name)
    
    image = cv2.imread(input_path)
    if image is None:
        raise ValueError("Could not read image file.")

    results = model(image, conf=conf_threshold)
    
    annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    for result in results:
        detections = sv.Detections.from_ultralytics(result)
        
        labels = [
            f"{model.names[class_id]} {confidence:0.2f}"
            for class_id, confidence in zip(detections.class_id, detections.confidence)
        ]
        
        image = annotator.annotate(scene=image, detections=detections)
        image = label_annotator.annotate(scene=image, detections=detections, labels=labels)

    cv2.imwrite(output_path, image)
    logger.info(f"Saved annotated image to {output_path}")


def process_video(input_path: str, output_path: str, model_name: str = "yolov8n.pt", conf_threshold: float = 0.25):
    """Processes a video through YOLOv8 and ByteTrack."""
    logger.info(f"Processing video {input_path} with {model_name}")
    model = get_model(model_name)
    
    tracker = sv.ByteTrack()
    box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    trace_annotator = sv.TraceAnnotator()

    video_info = sv.VideoInfo.from_video_path(input_path)
    
    def frame_processor(frame: iter):
        results = model(frame, conf=conf_threshold, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(results)
        detections = tracker.update_with_detections(detections)

        labels = [
            f"#{tracker_id} {model.names[class_id]} {confidence:0.2f}"
            for class_id, tracker_id, confidence
            in zip(detections.class_id, detections.tracker_id, detections.confidence)
            if tracker_id is not None
        ]
        
        annotated_frame = frame.copy()
        annotated_frame = trace_annotator.annotate(scene=annotated_frame, detections=detections)
        annotated_frame = box_annotator.annotate(scene=annotated_frame, detections=detections)
        annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
        
        return annotated_frame

    sv.process_video(
        source_path=input_path,
        target_path=output_path,
        callback=frame_processor
    )
    logger.info(f"Saved annotated video to {output_path}")
