from pydantic import BaseModel, HttpUrl, Field
from pydantic import EmailStr


class Organization(BaseModel):
    name: str
    website: HttpUrl | None = None
    phone: str | None = None
    email: EmailStr | None = None


class Booking(BaseModel):
    provider: Organization | None = None
    reference: str


class Coordinate(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
