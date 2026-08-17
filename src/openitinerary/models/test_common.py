import pytest
from pydantic import ValidationError

from openitinerary.models.common import Booking, Coordinate, LocalizedText, MultilingualText, Organization


def localized_text_payload() -> dict:
    return {
        "language": "en",
        "value": "Test value",
    }


def organization_payload() -> dict:
    return {
        "name": {"values": [{"language": "en", "value": "Test Organization"}]},
    }


@pytest.mark.parametrize("coordinate", [{"latitude": -90, "longitude": -180}, {"latitude": 90, "longitude": 180}])
def test_coordinate_accepts_boundary_values(coordinate: dict):
    result = Coordinate.model_validate(coordinate)

    assert result.latitude == coordinate["latitude"]
    assert result.longitude == coordinate["longitude"]


@pytest.mark.parametrize(
    "coordinate",
    [
        {"latitude": -90.1, "longitude": 0},
        {"latitude": 90.1, "longitude": 0},
        {"latitude": 0, "longitude": -180.1},
        {"latitude": 0, "longitude": 180.1},
    ],
)
def test_coordinate_rejects_out_of_range_values(coordinate: dict):
    with pytest.raises(ValidationError):
        Coordinate.model_validate(coordinate)


def test_localized_text_accepts_region():
    payload = localized_text_payload()
    payload["region"] = "PH"

    localized_text = LocalizedText.model_validate(payload)

    assert localized_text.language == "en"
    assert localized_text.region == "PH"


@pytest.mark.parametrize("field", ["language", "value"])
def test_localized_text_rejects_missing_required_fields(field: str):
    payload = localized_text_payload()
    del payload[field]

    with pytest.raises(ValidationError):
        LocalizedText.model_validate(payload)


@pytest.mark.parametrize("field", ["language", "region"])
def test_localized_text_rejects_invalid_language_or_region(field: str):
    payload = localized_text_payload()
    payload[field] = "invalid"

    with pytest.raises(ValidationError):
        LocalizedText.model_validate(payload)


@pytest.mark.parametrize("value", ["", []])
def test_multilingual_text_rejects_empty_values(value: str | list):
    with pytest.raises(ValidationError):
        MultilingualText.model_validate({"values": value})


def test_multilingual_text_rejects_duplicate_language_and_region_combination():
    with pytest.raises(ValidationError, match="each language and region combination must be unique"):
        MultilingualText.model_validate(
            {
                "values": [
                    {"language": "en", "value": "293 North Quay, Brisbane CBD, 4000"},
                    {"language": "en", "value": "Brisbane, Australia"},
                ]
            }
        )


def test_multilingual_text_accepts_same_language_with_different_regions():
    multilingual_text = MultilingualText.model_validate(
        {
            "values": [
                {"language": "en", "region": "AU", "value": "Brisbane QLD 4000"},
                {"language": "en", "region": "US", "value": "Brisbane, Queensland 4000"},
            ]
        }
    )

    assert [value.region for value in multilingual_text.values] == ["AU", "US"]


def test_organization_accepts_contact_details():
    payload = organization_payload()
    payload.update(
        {
            "website": "https://example.com/contact",
            "phone": "+6321234567",
            "email": "contact@example.com",
        }
    )

    organization = Organization.model_validate(payload)

    assert str(organization.website) == "https://example.com/contact"
    assert organization.phone == "+6321234567"
    assert organization.email == "contact@example.com"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("website", "not a URL"),
        ("email", "not an email"),
    ],
)
def test_organization_rejects_invalid_contact_details(field: str, value: str):
    payload = organization_payload()
    payload[field] = value

    with pytest.raises(ValidationError):
        Organization.model_validate(payload)


def test_booking_accepts_reference_without_provider():
    booking = Booking.model_validate({"reference": "ABC123"})

    assert booking.reference == "ABC123"
    assert booking.provider is None


def test_booking_rejects_missing_reference():
    with pytest.raises(ValidationError):
        Booking.model_validate({})
