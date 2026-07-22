from pydantic import BaseModel, HttpUrl, Field
from pydantic import EmailStr
from pydantic_extra_types.country import CountryAlpha2
from pydantic_extra_types.language_code import LanguageAlpha2


class LocalizedText(BaseModel):
    language: LanguageAlpha2
    region: CountryAlpha2 | None = None
    value: str


class MultilingualText(BaseModel):
    values: list[LocalizedText] = Field(min_length=1)


class Organization(BaseModel):
    name: MultilingualText
    website: HttpUrl | None = None
    phone: str | None = None
    email: EmailStr | None = None


class Booking(BaseModel):
    provider: Organization | None = None
    reference: str


class Coordinate(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
