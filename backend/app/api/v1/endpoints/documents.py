import shutil
import uuid
import os
from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from app.services.ingestion_service import process_document_pipeline

router = APIRouter()
UPLOAD_DIR = "./temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    doc_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{doc_id}_{file.filename}"
    
    # Lưu file vật lý
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Gọi service chạy ngầm
    background_tasks.add_task(
        process_document_pipeline, 
        file_path=file_path, 
        doc_id=doc_id, 
        filename=file.filename
    )
    
    # Phản hồi ngay cho Frontend (FR-01)
    return {
        "document_id": doc_id,
        "filename": file.filename,
        "status": "Uploading"
    }