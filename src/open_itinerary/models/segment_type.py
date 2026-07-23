from enum import StrEnum


class SegmentType(StrEnum):
    FLIGHT = "flight"
    ACCOMMODATION = "accommodation"
    # ACTIVITY = "activity"
    TRAIN = "train"
    # TRANSFER = "transfer"
    # CAR_RENTAL = "car_rental"
    # FERRY = "ferry"
    # CRUISE = "cruise"


class PlaceType(StrEnum):
    AIRPORT = "airport"
    TRAIN_STATION = "train_station"
