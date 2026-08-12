from open_itinerary.models.place import GenericPlace


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
