from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.videoSummarize.handleRequest import get_content

router = APIRouter()

# Define the request model
class GetVideoTranscriptRequest(BaseModel):
    url: str
    summaryOption: str
    explanationOption: str

@router.post("/getVideoTranscript", summary="Fetch video transcript and summary")
async def get_video_transcript(request: GetVideoTranscriptRequest):
    try:
        # Log the incoming request (optional for debugging)
        print(f"Processing request for URL: {request.url}")
        print(f"Summary Option: {request.summaryOption}")
        print(f"Explanation Option: {request.explanationOption}")
        
        # Call the get_content function and pass all relevant parameters
        content = get_content(
            url=request.url,
            summary_option=request.summaryOption,
            explanation_option=request.explanationOption,
        )

        # Return the processed content
        return {"content": content}
    except Exception as e:
        # Log the exception and raise an HTTP 500 error
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))