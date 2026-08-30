import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

from fastapi import Response

from openitinerary.adapters import Adapter
from openitinerary.adapters.api import mock as adapt_api
from openitinerary.models.domains.flight import FlightSegment


def _adapter(media_type: str = "application/pdf", segments: list | None = None) -> Mock:
    adapter = Mock(spec=Adapter)
    adapter.get_expected_media_types.return_value = {media_type}
    adapter.load = AsyncMock(return_value=[] if segments is None else segments)
    return adapter


def _upload(data: bytes, *, media_type: str = "application/pdf", size: int | None = None) -> SimpleNamespace:
    return SimpleNamespace(
        content_type=media_type,
        size=len(data) if size is None else size,
        read=AsyncMock(return_value=data),
        close=AsyncMock(),
    )


def test_adapt_mock_returns_fixed_segments_without_reading_upload():
    upload = _upload(b"ignored", media_type="text/plain")
    response = Response()

    actual = asyncio.run(adapt_api.adapt_mock(upload, response))

    assert len(actual) == 3
    assert all(isinstance(segment, FlightSegment) for segment in actual)
    assert [segment.flight_number for segment in actual] == ["PR101", "AD2898", "AD4056"]
    assert str(actual[0].id) == "cc09f4cd-5377-4bf5-a8fd-08b8b0c57e10"
    assert actual[0].start_place.iata_code == "HNL"
    assert actual[0].end_place.iata_code == "MNL"
    assert actual[1].start_place.iata_code == "SDU"
    assert actual[2].end_place.iata_code == "MAO"
    assert response.headers["X-Segment-Count"] == "3"
    upload.read.assert_not_awaited()
    upload.close.assert_awaited_once_with()
