import os
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Predict
from ..ai_model import pre_image

router = APIRouter(prefix="/predict", tags=["Prediction"])

UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
async def predict(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    label, con_score = pre_image(file_path)

    record = Predict(image_path=file_path, predict_label=label, con_score=con_score)
    db.add(record)
    db.commit()
    db.refresh(record)

    return {"label": label, "con_score": con_score, "image_path": file_path}

