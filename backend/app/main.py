from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.api.v1.endpoints import documents

app = FastAPI(title="AI Learning Assistant - Backend")

app.include_router(
    documents.router, 
    prefix="/api/v1/documents", 
    tags=["Documents"]
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Backend đang chạy ngon lành!"}