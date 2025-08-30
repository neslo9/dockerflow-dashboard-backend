from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, images
from .database import init_db

app = FastAPI(title="DockerFlow API")

app.include_router(auth.router)
app.include_router(images.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.1.100:30008"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
    
@app.on_event("startup")
def startup_event():
    init_db()
