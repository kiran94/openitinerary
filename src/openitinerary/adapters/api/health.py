from fastapi.routing import APIRouter
from pydantic import BaseModel

router = APIRouter()

_TAGS = ["health"]


class LiveResponse(BaseModel):
    status: str


class ChecksResponse(BaseModel):
    pass


class ReadyResponse(LiveResponse):
    checks: list[ChecksResponse]


@router.get("/live", response_model=LiveResponse, tags=_TAGS)
async def live() -> LiveResponse:
    return LiveResponse(status="up")


@router.get("/ready", response_model=ReadyResponse, tags=_TAGS)
async def ready() -> ReadyResponse:
    return ReadyResponse(status="up", checks=[])
