from pydantic import BaseModel, EmailStr, Field, HttpUrl
from pydantic_extra_types.country import CountryAlpha2
from pydantic_extra_types.language_code import LanguageAlpha2


class LocalizedText(BaseModel):
    language: LanguageAlpha2
    region: CountryAlpha2 | None = None
    value: str = Field(min_length=1)


class MultilingualText(BaseModel):
    values: list[LocalizedText] = Field(min_length=1)


class Organization(BaseModel):
    name: MultilingualText = Field(description="The name of the Organization")
    website: HttpUrl | None = Field(description="The website of the Organization", default=None)
    phone: str | None = Field(description="The phone number of the Organization (with country code)", default=None)
    email: EmailStr | None = Field(description="The email of the Organization", default=None)


class Booking(BaseModel):
    provider: Organization | None = Field(
        description="The intermediary or organization through which the booking was made, such as booking.com, Expedia, GetYourGuide, directly with an airline or any other travel agency/platfo or any other travel agency/platform",
        default=None,
    )
    reference: str = Field(description="The booking confirmation/reference code used by the traveller.")


class Coordinate(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
