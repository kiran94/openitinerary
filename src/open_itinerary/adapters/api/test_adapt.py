import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException, Response, status

from open_itinerary.adapters import Adapter, InputContent
from open_itinerary.adapters.api import adapt as adapt_api


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


@pytest.mark.parametrize("size", [3, 4])
@patch("open_itinerary.adapters.api.adapt.OPEN_ITINERARY_MAX_UPLOAD_SIZE_BYTES", 4)
@patch("open_itinerary.adapters.api.adapt.ALL_ADAPTERS", new_callable=list)
def test_adapt_accepts_files_up_to_the_configured_limit(all_adapters: list[Adapter], size: int):
    adapter = _adapter(segments=[Mock(name="segment")])
    all_adapters.append(adapter)
    upload = _upload(b"x" * size)
    response = Response()

    actual = asyncio.run(adapt_api.adapt(upload, response))

    assert actual == adapter.load.return_value
    upload.read.assert_awaited_once_with(5)
    upload.close.assert_awaited_once_with()
    adapter.load.assert_awaited_once_with(InputContent(b"x" * size, "application/pdf"))
    assert response.headers["X-Segment-Count"] == "1"


@patch("open_itinerary.adapters.api.adapt.OPEN_ITINERARY_MAX_UPLOAD_SIZE_BYTES", 4)
@patch("open_itinerary.adapters.api.adapt.ALL_ADAPTERS", new_callable=list)
def test_adapt_rejects_known_oversized_file_without_reading(all_adapters: list[Adapter]):
    adapter = _adapter()
    all_adapters.append(adapter)
    upload = _upload(b"", size=5)

    with pytest.raises(HTTPException) as e:
        asyncio.run(adapt_api.adapt(upload, Response()))

    assert e.value.status_code == status.HTTP_413_CONTENT_TOO_LARGE
    assert e.value.detail == "Uploaded file exceeds the configured limit of 4 bytes"

    upload.read.assert_not_awaited()
    upload.close.assert_awaited_once_with()
    adapter.load.assert_not_awaited()


@patch("open_itinerary.adapters.api.adapt.OPEN_ITINERARY_MAX_UPLOAD_SIZE_BYTES", 4)
@patch("open_itinerary.adapters.api.adapt.ALL_ADAPTERS", new_callable=list)
def test_adapt_rejects_oversized_file_when_size_is_unknown(all_adapters: list[Adapter]):
    adapter = _adapter()
    all_adapters.append(adapter)
    upload = _upload(b"12345")
    upload.size = None

    with pytest.raises(HTTPException) as e:
        asyncio.run(adapt_api.adapt(upload, Response()))

    assert e.value.status_code == status.HTTP_413_CONTENT_TOO_LARGE
    upload.read.assert_awaited_once_with(5)
    upload.close.assert_awaited_once_with()
    adapter.load.assert_not_awaited()


@patch("open_itinerary.adapters.api.adapt.ALL_ADAPTERS", new_callable=list)
def test_adapt_rejects_unsupported_media_type_without_reading(all_adapters: list[Adapter]):
    adapter = _adapter()
    all_adapters.append(adapter)
    upload = _upload(b"content", media_type="text/plain")

    with pytest.raises(HTTPException) as e:
        asyncio.run(adapt_api.adapt(upload, Response()))

    assert e.value.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    upload.read.assert_not_awaited()
    upload.close.assert_awaited_once_with()
    adapter.load.assert_not_awaited()


@patch("open_itinerary.adapters.api.adapt.ALL_ADAPTERS", new_callable=list)
def test_adapt_closes_upload_when_adapter_fails(all_adapters: list[Adapter]):
    adapter = _adapter()
    adapter.load.side_effect = RuntimeError("adapter failed")
    all_adapters.append(adapter)
    upload = _upload(b"content")

    with pytest.raises(RuntimeError, match="adapter failed"):
        asyncio.run(adapt_api.adapt(upload, Response()))

    upload.close.assert_awaited_once_with()
