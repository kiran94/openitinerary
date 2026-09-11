from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from openitinerary.adapters.api import adapt, mock, telemetry
from openitinerary.version import __version__


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        telemetry.shutdown()


app = FastAPI(title="OpenItinerary Adapter API", version=__version__, debug=False, lifespan=lifespan)
telemetry.setup_libraries(app)

app.include_router(adapt.router, prefix="/api/v1/adapt")
app.include_router(mock.router, prefix="/api/v1/mock")


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse("/docs")
