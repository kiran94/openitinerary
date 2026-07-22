from pydantic import BaseModel
from pydantic_extra_types.country import CountryAlpha2
from pydantic_extra_types.timezone_name import TimeZoneName
from open_itinerary.models.common import Coordinate, MultilingualText


class Place(BaseModel):
    name: MultilingualText
    country: CountryAlpha2
    timezone: TimeZoneName
    coordinate: Coordinate
