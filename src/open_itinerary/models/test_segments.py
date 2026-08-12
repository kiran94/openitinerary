from uuid import uuid4

import pytest
from pydantic import ValidationError

from open_itinerary.models.segments import BaseSegment


def segment_payload() -> dict:
    return {
        "id": str(uuid4()),
        "type": "activity",
        "title": {"values": [{"language": "en", "value": "Museum visit"}]},
        "start_time_utc": "2026-08-07T03:00:00Z",
    }


def test_base_segment_requires_uuid():
    payload = segment_payload()
    del payload["id"]

    with pytest.raises(ValidationError):
        BaseSegment.model_validate(payload)


def test_base_segment_rejects_invalid_uuid():
    payload = segment_payload()
    payload["id"] = "not-a-uuid"

    with pytest.raises(ValidationError):
        BaseSegment.model_validate(payload)


def test_base_segment_rejects_unknown_fields():
    payload = segment_payload()
    payload["unknown_field"] = "unexpected"

    with pytest.raises(ValidationError):
        BaseSegment.model_validate(payload)


def test_base_segment_is_frozen():
    segment = BaseSegment.model_validate(segment_payload())

    with pytest.raises(ValidationError):
        segment.start_time_utc = "2026-08-08T03:00:00Z"


def test_base_segment_round_trips_optional_fields():
    payload = segment_payload()
    payload.update(
        {
            "description": {"values": [{"language": "en", "value": "Timed entry"}]},
            "end_time_utc": "2026-08-07T05:00:00Z",
            "operator": {
                "name": {"values": [{"language": "en", "value": "National Museum"}]},
                "website": "https://museum.example.com",
                "phone": "+6321234567",
                "email": "contact@museum.example.com",
            },
            "booking": {
                "provider": {"name": {"values": [{"language": "en", "value": "Ticket Provider"}]}},
                "reference": "ABC123",
            },
        }
    )

    segment = BaseSegment.model_validate(payload)
    round_tripped_segment = BaseSegment.model_validate_json(segment.model_dump_json())

    assert round_tripped_segment == segment
    assert round_tripped_segment.description.values[0].value == "Timed entry"
    assert round_tripped_segment.operator.email == "contact@museum.example.com"
    assert round_tripped_segment.booking.reference == "ABC123"


def test_base_segment_serializes_utc_timestamps():
    payload = segment_payload()
    payload["end_time_utc"] = "2026-08-07T05:00:00Z"

    segment = BaseSegment.model_validate(payload)

    assert segment.model_dump(mode="json")["start_time_utc"] == "2026-08-07T03:00:00Z"
    assert segment.model_dump(mode="json")["end_time_utc"] == "2026-08-07T05:00:00Z"
