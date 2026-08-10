from typing import Annotated

from pydantic import Field

from open_itinerary.models.domains.flight import AirportPlace
from open_itinerary.models.domains.train import TrainStation
from open_itinerary.models.place import GenericPlace

Place = Annotated[GenericPlace | AirportPlace | TrainStation, Field(discriminator="type")]
