from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import os
import shutil
import uuid
from app.core.config import settings
from app.services.inference import process_image, process_video

router = APIRouter()

class DetectionResult(BaseModel):
    id: str
    filename: str
    status: str
    type: str

@router.post("/image", response_model=DetectionResult)
async def detect_image(
    file: UploadFile = File(...),
    model_name: str = "yolov8n.pt",
    conf_threshold: float = 0.25
):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Only images allowed (PNG, JPG, JPEG)")
    
    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    input_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
    output_path = os.path.join(settings.OUTPUT_DIR, f"{file_id}{ext}")

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process image synchronously for now
    try:
        process_image(input_path, output_path, model_name, conf_threshold)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

    return DetectionResult(
        id=file_id,
        filename=file.filename,
        status="completed",
        type="image"
    )

@router.post("/video", response_model=DetectionResult)
async def detect_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    model_name: str = "yolov8n.pt",
    conf_threshold: float = 0.25
):
    if not file.filename.lower().endswith(('.mp4', '.avi', '.mov')):
        raise HTTPException(status_code=400, detail="Only videos allowed (MP4, AVI, MOV)")
    
    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    input_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
    output_path = os.path.join(settings.OUTPUT_DIR, f"{file_id}{ext}")

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process video asynchronously since it takes time
    background_tasks.add_task(process_video, input_path, output_path, model_name, conf_threshold)

    return DetectionResult(
        id=file_id,
        filename=file.filename,
        status="processing",
        type="video"
    )

@router.get("/result/{file_id}")
async def get_result(file_id: str):
    # Find the file in the output directory
    for f in os.listdir(settings.OUTPUT_DIR):
        if f.startswith(file_id):
            return FileResponse(os.path.join(settings.OUTPUT_DIR, f))
    
    raise HTTPException(status_code=404, detail="Result not found or still processing")
