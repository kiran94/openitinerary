import pytest

from open_itinerary.models.place import BasePlace, GenericPlace


def test_place_formatted_address_supports_source_language_variants():
    place = GenericPlace.model_validate(
        {
            "name": {"values": [{"language": "en", "value": "Best Western Hotel Fino Tokyo Akihabara"}]},
            "formatted_address": {
                "values": [
                    {"language": "en", "value": "Taito-ku, Ueno 5-1-6, Taito Ward, Tokyo, 110-0005, Japan"},
                    {"language": "ja", "value": "台東区上野 5-1-6, 台東区, 東京都"},
                ]
            },
            "country": "JP",
            "timezone": "Asia/Tokyo",
            "coordinate": {"latitude": 35.7032, "longitude": 139.7755},
            "type": "location",
        }
    )

    assert [value.language for value in place.formatted_address.values] == ["en", "ja"]


@pytest.mark.parametrize(
    "input,expected_output",
    [
        pytest.param(
            "Taito-ku, Ueno 5-1-6,\nTaito Ward, \nTokyo, \n110-0005, \nJapan",
            "Taito-ku, Ueno 5-1-6, Taito Ward,  Tokyo,  110-0005,  Japan",
            id="unix_new_lines",
        ),
        pytest.param(
            "Taito-ku, Ueno 5-1-6, \r\nTaito Ward, \r\nTokyo, \r\n110-0005, \r\nJapan",
            "Taito-ku, Ueno 5-1-6,  Taito Ward,  Tokyo,  110-0005,  Japan",
            id="window_new_lines",
        ),
    ],
)
def test_place_formatted_address_whitespace(input: str, expected_output: str):

    place = BasePlace.model_validate(
        {
            "name": {"values": [{"language": "en", "value": "Best Western Hotel Fino Tokyo Akihabara"}]},
            "formatted_address": {
                "values": [
                    {"language": "en", "value": input},
                ]
            },
            "country": "JP",
            "timezone": "Asia/Tokyo",
            "coordinate": {"latitude": 35.7032, "longitude": 139.7755},
            "type": "location",
        }
    )

    assert len(place.formatted_address.values) == 1
    assert place.formatted_address.values[0].value == expected_output


def test_place_formatted_address_none():
    place = BasePlace.model_validate(
        {
            "name": {"values": [{"language": "en", "value": "Best Western Hotel Fino Tokyo Akihabara"}]},
            "formatted_address": None,
            "country": "JP",
            "timezone": "Asia/Tokyo",
            "coordinate": {"latitude": 35.7032, "longitude": 139.7755},
            "type": "location",
        }
    )

    validated_place = BasePlace.model_validate(place)
    assert not validated_place.formatted_address
