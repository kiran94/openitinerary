from typing import Annotated

from pydantic import Field

from openitinerary.models.domains.flight import AirportPlace
from openitinerary.models.domains.train import TrainStation
from openitinerary.models.place import GenericPlace

Place = Annotated[GenericPlace | AirportPlace | TrainStation, Field(discriminator="type")]
