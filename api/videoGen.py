from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.videoEngine.engine.video_engine import getSource
from services.videoEngine.utils.db_utils import getDrafts, getProjectDraft

router = APIRouter()


#API to get the source selection from user and then send info back
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
    
#api to get all draft sitting in db
@router.get("/getDraft", summary="Fetch all draft projects")
async def get_projects():
    try:
        drafts = getDrafts()
        print("Got drafts")
        return{"content":drafts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class GetProjectDraftRequest(BaseModel):
    id: str

@router.post("/getDraftProject", summary="Fetch entire project draft data")
async def get_draft_project(request: GetProjectDraftRequest):
    try:
        # Call the getProjectDraft function with the provided id
        print(request.id)
        project, status_code = getProjectDraft(request.id)

        if status_code == 404:
            raise HTTPException(status_code=404, detail=project["error"])
        elif status_code == 500:
            raise HTTPException(status_code=500, detail=project["error"])

        return project  # Return the entire project document

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


