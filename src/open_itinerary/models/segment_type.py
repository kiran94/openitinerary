from enum import StrEnum


class SegmentType(StrEnum):
    FLIGHT = "flight"
    ACCOMMODATION = "accommodation"
    TRAIN = "train"
    TRANSFER = "transfer"
    # ACTIVITY = "activity"
    # CAR_RENTAL = "car_rental"
    # FERRY = "ferry"
    # CRUISE = "cruise"


class PlaceType(StrEnum):
    LOCATION = "location"
    AIRPORT = "airport"
    TRAIN_STATION = "train_station"
