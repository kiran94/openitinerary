from uuid import uuid4

import pytest
from pydantic import ValidationError

from open_itinerary.models.domains.flight import AirportPlace
from open_itinerary.models.domains.train import TrainStation
from open_itinerary.models.domains.transfer import TransferMode, TransferSegment
from open_itinerary.models.place import GenericPlace


def place_payload(place_type: str = "location") -> dict:
    return {
        "type": place_type,
        "name": {"values": [{"language": "en", "value": "Test place"}]},
        "country": "PH",
        "timezone": "Asia/Manila",
        "coordinate": {"latitude": 14.5995, "longitude": 120.9842},
    }


def transfer_payload() -> dict:
    return {
        "id": str(uuid4()),
        "type": "transfer",
        "title": {"values": [{"language": "en", "value": "Airport transfer"}]},
        "start_time_utc": "2026-08-07T03:00:00Z",
        "start_place": place_payload(),
        "end_place": place_payload(),
        "transfer_mode": "taxi",
    }


@pytest.mark.parametrize("transfer_mode", list(TransferMode))
def test_transfer_segment_accepts_each_mode(transfer_mode: TransferMode):
    payload = transfer_payload()
    payload["transfer_mode"] = transfer_mode.value

    segment = TransferSegment.model_validate(payload)

    assert segment.transfer_mode == transfer_mode


@pytest.mark.parametrize(
    ("place_type", "expected_type"),
    [
        ("location", GenericPlace),
        ("airport", AirportPlace),
        ("train_station", TrainStation),
    ],
)
def test_transfer_segment_accepts_all_place_variants(place_type: str, expected_type: type):
    payload = transfer_payload()
    payload["start_place"] = place_payload(place_type)
    payload["end_place"] = place_payload(place_type)

    segment = TransferSegment.model_validate(payload)

    assert isinstance(segment.start_place, expected_type)
    assert isinstance(segment.end_place, expected_type)


def test_transfer_segment_rejects_unknown_mode():
    payload = transfer_payload()
    payload["transfer_mode"] = "limousine"

    with pytest.raises(ValidationError):
        TransferSegment.model_validate(payload)


@pytest.mark.parametrize("field", ["start_place", "end_place"])
def test_transfer_segment_rejects_missing_field(field: str):
    payload = transfer_payload()
    del payload[field]

    with pytest.raises(ValidationError):
        TransferSegment.model_validate(payload)


@pytest.mark.parametrize("field", ["start_place", "end_place"])
def test_transfer_segment_rejects_null_field(field: str):
    payload = transfer_payload()
    payload[field] = None

    with pytest.raises(ValidationError):
        TransferSegment.model_validate(payload)
