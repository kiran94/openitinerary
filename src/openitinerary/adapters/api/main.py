from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from openitinerary.adapters.api import adapt

app = FastAPI(title="OpenItinerary Adapter API")

app.include_router(adapt.router, prefix="/api/v1/adapt")


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse("/docs")
