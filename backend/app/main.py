from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Database
from app.routes import dictionary, history
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Meitei Mayek Dictionary API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(dictionary.router)
app.include_router(history.router)

@app.on_event("startup")
async def startup_db():
    await Database.connect()

@app.on_event("shutdown")
async def shutdown_db():
    await Database.close()

@app.get("/")
async def root():
    return {"message": "Meitei Mayek Dictionary API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}