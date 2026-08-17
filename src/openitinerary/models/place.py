from typing import Literal

from pydantic import BaseModel, Field, field_validator
from pydantic_extra_types.country import CountryAlpha2
from pydantic_extra_types.timezone_name import TimeZoneName

from openitinerary.models.common import Coordinate, MultilingualText
from openitinerary.models.segment_type import PlaceType


class BasePlace(BaseModel):
    name: MultilingualText = Field(description="The name of the place")
    country: CountryAlpha2
    timezone: TimeZoneName
    coordinate: Coordinate
    formatted_address: MultilingualText | None = Field(
        default=None, description="The place's formatted postal or street address, as supplied by the provider."
    )

    @field_validator("formatted_address", mode="after")
    @classmethod
    def clean_formatted_address(cls, obj: MultilingualText) -> MultilingualText:
        if not obj:
            return None

        for current_lang in obj.values:
            current_lang.value = current_lang.value.replace("\r\n", " ")
            current_lang.value = current_lang.value.replace("\n", " ")

        return obj


class GenericPlace(BasePlace):
    type: Literal[PlaceType.LOCATION] = PlaceType.LOCATION
