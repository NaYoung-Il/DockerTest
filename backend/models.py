from .db import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, func

class Predict(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String(255), nullable=False)
    predict_label = Column(String(100), nullable=False)
    con_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now())