from uuid import uuid4

import pytest
from pydantic import ValidationError

from open_itinerary.models.domains.activity import ActivitySegment
from open_itinerary.models.itinerary import Itinerary
from open_itinerary.version import OPEN_ITINERARY_VERSION


def activity_payload(name: str = "Museum visit", start_time_utc: str = "2026-08-07T03:00:00Z") -> dict:
    return {
        "id": str(uuid4()),
        "type": "activity",
        "title": {"values": [{"language": "en", "value": name}]},
        "start_time_utc": start_time_utc,
        "place": {
            "type": "location",
            "name": {"values": [{"language": "en", "value": "Test place"}]},
            "country": "PH",
            "timezone": "Asia/Manila",
            "coordinate": {"latitude": 14.5995, "longitude": 120.9842},
        },
    }


def itinerary_payload() -> dict:
    return {
        "id": "test-itinerary",
        "title": "Test itinerary",
        "segments": [activity_payload()],
    }


def test_itinerary_defaults_to_current_schema_version():
    itinerary = Itinerary.model_validate(itinerary_payload())

    assert itinerary.schema_version == OPEN_ITINERARY_VERSION


def test_itinerary_accepts_empty_segments():
    itinerary = Itinerary.model_validate(
        {
            "id": None,
            "title": None,
            "segments": [],
        }
    )

    assert itinerary.segments == []


def test_itinerary_rejects_unknown_segment_type():
    payload = itinerary_payload()
    payload["segments"][0]["type"] = "ferry"

    with pytest.raises(ValidationError):
        Itinerary.model_validate(payload)


def test_itinerary_rejects_malformed_segment_payload():
    payload = itinerary_payload()
    del payload["segments"][0]["place"]

    with pytest.raises(ValidationError):
        Itinerary.model_validate(payload)


def test_itinerary_rejects_non_string_schema_version():
    payload = itinerary_payload()
    payload["schema_version"] = 2

    with pytest.raises(ValidationError):
        Itinerary.model_validate(payload)


def test_itinerary_preserves_created_and_updated_timestamps():
    payload = itinerary_payload()
    payload["created_at"] = "2026-08-01T03:00:00Z"
    payload["updated_at"] = "2026-08-02T03:00:00Z"

    itinerary = Itinerary.model_validate(payload)

    assert itinerary.model_dump(mode="json")["created_at"] == "2026-08-01T03:00:00Z"
    assert itinerary.model_dump(mode="json")["updated_at"] == "2026-08-02T03:00:00Z"


def test_itinerary_preserves_segment_order():
    payload = itinerary_payload()
    payload["segments"] = [
        activity_payload("Second activity", "2026-08-07T05:00:00Z"),
        activity_payload("First activity", "2026-08-07T03:00:00Z"),
    ]

    itinerary = Itinerary.model_validate(payload)

    assert all(isinstance(segment, ActivitySegment) for segment in itinerary.segments)
    assert [segment.title.values[0].value for segment in itinerary.segments] == ["Second activity", "First activity"]
