from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from openitinerary.adapters.api import adapt, mock

app = FastAPI(title="OpenItinerary Adapter API", debug=False)

app.include_router(adapt.router, prefix="/api/v1/adapt")
app.include_router(mock.router, prefix="/api/v1/mock")


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse("/docs")
