from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from backend.db import engine
from backend.models import Base
from backend.routers import predict
from .db import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Image")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(predict.router)

@app.get("/")
def root():
    return {"message": "AI Image"}