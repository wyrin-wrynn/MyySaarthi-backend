from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.heartbeat import router as heartbeat_router
from app.api.videoGen import router as videogen_router

app = FastAPI(
    title="Video Generation API",
    description="Backend APIs for Video Generation",
    version="1.0.0"
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific origins in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routes
app.include_router(heartbeat_router, prefix="/api/v1")
app.include_router(videogen_router, prefix="/api/v1")

# Root Endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Video Generation API!"}
