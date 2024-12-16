from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.heartbeat import router as heartbeat_router
from api.videoGen import router as videogen_router
from api.videoSummarize import router as videoSummarize_router
import uvicorn

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
app.include_router(videoSummarize_router, prefix="/api/v1")

# Root Endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Video Generation API!"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3050,
        reload=True,
        timeout_keep_alive=600,  # Set timeout to 300 seconds (5 minutes)
    )
