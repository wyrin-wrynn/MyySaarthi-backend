from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.videoEngine.engine.video_engine import getSource

router = APIRouter()

class GetSourceRequest(BaseModel):
    source: str
    url: str
    aspect: str
    duration: int

@router.post("/getSource", summary="Fetch source content")
async def get_source(request: GetSourceRequest):
    try:
        # Call the getSource function with provided parameters
        content = getSource(
            source=request.source,
            url=request.url,
            aspect=request.aspect,
            duration=request.duration
        )
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

class DraftResponses(BaseModel):
    id: str
    url: str
    title: str

