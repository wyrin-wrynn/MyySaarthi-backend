from fastapi import APIRouter

router = APIRouter()

@router.get("/heartbeat", summary="Heartbeat Endpoint")
async def heartbeat():
    return {"status": "alive"}
