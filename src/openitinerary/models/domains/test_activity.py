from uuid import uuid4

import pytest
from pydantic import ValidationError

from openitinerary.models.domains.activity import ActivitySegment, ActivityType, TourSegment
from openitinerary.models.domains.flight import AirportPlace
from openitinerary.models.domains.train import TrainStation
from openitinerary.models.itinerary import Itinerary
from openitinerary.models.place import GenericPlace
from openitinerary.version import OPEN_ITINERARY_SCHEMA_URL


def place_payload(place_type: str = "location", name: str = "Test place") -> dict:
    return {
        "type": place_type,
        "name": {"values": [{"language": "en", "value": name}]},
        "country": "PH",
        "timezone": "Asia/Manila",
        "coordinate": {"latitude": 14.5995, "longitude": 120.9842},
    }


def activity_payload() -> dict:
    return {
        "id": str(uuid4()),
        "type": "activity",
        "title": {"values": [{"language": "en", "value": "Museum visit"}]},
        "start_time_utc": "2026-08-07T03:00:00Z",
        "place": place_payload(),
        "activity_type": "attraction",
    }


def tour_payload() -> dict:
    return {
        "id": str(uuid4()),
        "type": "tour",
        "title": {"values": [{"language": "en", "value": "City tour"}]},
        "start_time_utc": "2026-08-07T03:00:00Z",
        "place": place_payload(name="Meeting point"),
    }


@pytest.mark.parametrize("activity_type", list(ActivityType))
def test_activity_segment_accepts_each_activity_type(activity_type: ActivityType):
    payload = activity_payload()
    payload["activity_type"] = activity_type.value

    segment = ActivitySegment.model_validate(payload)

    assert segment.activity_type == activity_type


def test_activity_segment_rejects_unknown_activity_type():
    payload = activity_payload()
    payload["activity_type"] = "sport"

    with pytest.raises(ValidationError):
        ActivitySegment.model_validate(payload)


def test_activity_segment_defaults_to_unclassified():
    payload = activity_payload()
    del payload["activity_type"]

    segment = ActivitySegment.model_validate(payload)

    assert segment.activity_type is None


@pytest.mark.parametrize("field", ["place"])
def test_activity_segment_rejects_missing_or_null_place(field: str):
    payload = activity_payload()
    del payload[field]

    with pytest.raises(ValidationError):
        ActivitySegment.model_validate(payload)

    payload = activity_payload()
    payload[field] = None

    with pytest.raises(ValidationError):
        ActivitySegment.model_validate(payload)


def test_tour_segment_defaults_to_no_stops():
    segment = TourSegment.model_validate(tour_payload())

    assert segment.stops is None
    assert segment.drop_off_place is None


@pytest.mark.parametrize(
    ("place_type", "expected_type"),
    [
        ("location", GenericPlace),
        ("airport", AirportPlace),
        ("train_station", TrainStation),
    ],
)
def test_tour_segment_preserves_ordered_stops(place_type: str, expected_type: type):
    payload = tour_payload()
    payload["stops"] = [
        place_payload(place_type, "First stop"),
        place_payload(place_type, "Second stop"),
    ]

    segment = TourSegment.model_validate(payload)

    assert all(isinstance(place, expected_type) for place in segment.stops)
    assert [place.name.values[0].value for place in segment.stops] == ["First stop", "Second stop"]


def test_tour_segment_rejects_malformed_stop():
    payload = tour_payload()
    payload["stops"] = [{"type": "location"}]

    with pytest.raises(ValidationError):
        TourSegment.model_validate(payload)


@pytest.mark.parametrize(
    ("place_type", "expected_type"),
    [
        ("location", GenericPlace),
        ("airport", AirportPlace),
        ("train_station", TrainStation),
    ],
)
def test_tour_segment_accepts_drop_off_place(place_type: str, expected_type: type):
    payload = tour_payload()
    payload["drop_off_place"] = place_payload(place_type, "Drop-off point")

    segment = TourSegment.model_validate(payload)

    assert isinstance(segment.drop_off_place, expected_type)
    assert segment.drop_off_place.name.values[0].value == "Drop-off point"


def test_tour_segment_rejects_malformed_drop_off_place():
    payload = tour_payload()
    payload["drop_off_place"] = {"type": "location"}

    with pytest.raises(ValidationError):
        TourSegment.model_validate(payload)


@pytest.mark.parametrize("field", ["place"])
def test_tour_segment_rejects_missing_or_null_meeting_place(field: str):
    payload = tour_payload()
    del payload[field]

    with pytest.raises(ValidationError):
        TourSegment.model_validate(payload)

    payload = tour_payload()
    payload[field] = None

    with pytest.raises(ValidationError):
        TourSegment.model_validate(payload)


def test_itinerary_parses_activity_and_tour_segments():
    tour = tour_payload()
    tour["stops"] = [place_payload(name="Tour stop")]
    tour["drop_off_place"] = place_payload(name="Drop-off point")

    itinerary = Itinerary.model_validate(
        {
            "$schema": OPEN_ITINERARY_SCHEMA_URL,
            "id": "test-itinerary",
            "title": "Test itinerary",
            "segments": [activity_payload(), tour],
        }
    )

    assert isinstance(itinerary.segments[0], ActivitySegment)
    assert isinstance(itinerary.segments[1], TourSegment)
    assert itinerary.segments[1].place.name.values[0].value == "Meeting point"
    assert itinerary.segments[1].stops[0].name.values[0].value == "Tour stop"
    assert itinerary.segments[1].drop_off_place.name.values[0].value == "Drop-off point"
