from pydantic import BaseModel, Field
from pydantic_extra_types.country import CountryAlpha2
from pydantic_extra_types.timezone_name import TimeZoneName
from open_itinerary.models.common import Coordinate, MultilingualText


class Place(BaseModel):
    name: MultilingualText = Field(description="The name of the place")
    country: CountryAlpha2
    timezone: TimeZoneName
    coordinate: Coordinate
