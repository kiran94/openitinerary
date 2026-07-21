from open_itinerary.models.itinerary import Itinerary
import json


def main() -> None:
    schema = Itinerary.model_json_schema()
    print(json.dumps(schema))
