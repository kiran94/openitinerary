from pydantic import BaseModel
from pydantic_extra_types.country import CountryAlpha2
from pydantic_extra_types.timezone_name import TimeZoneName
from open_itinerary.models.common import Coordinate


class Place(BaseModel):
    name: str
    country: CountryAlpha2
    timezone: TimeZoneName
    coordinate: Coordinate
