import logging

from fastapi import APIRouter, Response, UploadFile
from opentelemetry import metrics, trace

from openitinerary.models.domains.flight import FlightSegment
from openitinerary.models.itinerary import Segment

router = APIRouter()

_TAGS = ["Mock"]


_meter = metrics.get_meter(__name__)
mock_metric = _meter.create_histogram("oi.document.input.size.mock", "By")
tracer = trace.get_tracer(__name__)


@router.post("/segment-mock", response_model=list[Segment], tags=_TAGS, include_in_schema=False)
async def adapt_mock(file: UploadFile, response: Response) -> list[Segment]:
    logger = logging.getLogger(__name__)

    logger.info("running adapter mock")
    mock_metric.record(file.size, {"content_type": file.content_type})

    with tracer.start_as_current_span("mock segment") as span:
        span.set_attribute("file.size.bytes", file.size)
        try:
            segments: list[Segment] = _MOCK_SEGMENTS
            response.headers["X-Segment-Count"] = str(len(segments))
            return segments
        finally:
            await file.close()


_MOCK_SEGMENTS: list[FlightSegment] = [
    FlightSegment.model_validate(
        {
            "id": "cc09f4cd-5377-4bf5-a8fd-08b8b0c57e10",
            "type": "flight",
            "title": {
                "values": [{"language": "en", "region": None, "value": "Philippine Airlines PR101: Honolulu to Manila"}]
            },
            "description": {
                "values": [
                    {
                        "language": "en",
                        "region": None,
                        "value": "Economy (U); duration 10h 55m. Hand baggage up to 7 kg and first and second "
                        "checked bags up to 23 kg each included.",
                    }
                ]
            },
            "start_time_utc": "2026-07-30T23:10:00Z",
            "end_time_utc": "2026-07-31T10:05:00Z",
            "operator": {
                "name": {"values": [{"language": "en", "region": None, "value": "Philippine Airlines"}]},
                "website": "https://www.philippineairlines.com/",
                "phone": None,
                "email": None,
            },
            "booking": {
                "provider": {
                    "name": {"values": [{"language": "en", "region": None, "value": "Expedia"}]},
                    "website": "https://www.expedia.com/",
                    "phone": "+443301231235",
                    "email": None,
                },
                "reference": "73480142822407",
            },
            "start_place": {
                "name": {
                    "values": [{"language": "en", "region": None, "value": "Daniel K. Inouye International Airport"}]
                },
                "country": "US",
                "timezone": "Pacific/Honolulu",
                "coordinate": {"latitude": 21.3187, "longitude": -157.9225},
                "type": "airport",
                "iata_code": "HNL",
                "icao_code": "PHNL",
            },
            "end_place": {
                "name": {"values": [{"language": "en", "region": None, "value": "Ninoy Aquino International Airport"}]},
                "country": "PH",
                "timezone": "Asia/Manila",
                "coordinate": {"latitude": 14.5086, "longitude": 121.0198},
                "type": "airport",
                "iata_code": "MNL",
                "icao_code": "RPLL",
            },
            "flight_number": "PR101",
            "pnr": "9EK2B4",
        }
    ),
    FlightSegment.model_validate(
        {
            "id": "f2c43a87-704b-4a75-a2a2-fd78fa698563",
            "type": "flight",
            "title": {"values": [{"language": "en", "region": None, "value": "Azul 2898: Rio de Janeiro to Campinas"}]},
            "description": {
                "values": [
                    {
                        "language": "en",
                        "region": None,
                        "value": "Economy (Y). Expedia itinerary: 73471665920059.",
                    }
                ]
            },
            "start_time_utc": "2026-07-14T13:05:00Z",
            "end_time_utc": "2026-07-14T14:15:00Z",
            "operator": {
                "name": {"values": [{"language": "en", "region": None, "value": "Azul"}]},
                "website": "https://www.voeazul.com.br/",
                "phone": None,
                "email": None,
            },
            "booking": {
                "provider": {
                    "name": {"values": [{"language": "en", "region": None, "value": "Expedia"}]},
                    "website": None,
                    "phone": "0330 123 1235",
                    "email": None,
                },
                "reference": "AEPL9L",
            },
            "start_place": {
                "name": {"values": [{"language": "en", "region": None, "value": "Santos Dumont Airport"}]},
                "country": "BR",
                "timezone": "America/Sao_Paulo",
                "coordinate": {"latitude": -22.91, "longitude": -43.1631},
                "type": "airport",
                "iata_code": "SDU",
                "icao_code": "SBRJ",
            },
            "end_place": {
                "name": {
                    "values": [
                        {
                            "language": "en",
                            "region": None,
                            "value": "Viracopos - Campinas International Airport",
                        }
                    ]
                },
                "country": "BR",
                "timezone": "America/Sao_Paulo",
                "coordinate": {"latitude": -23.0074, "longitude": -47.1345},
                "type": "airport",
                "iata_code": "VCP",
                "icao_code": "SBKP",
            },
            "flight_number": "AD2898",
        }
    ),
    FlightSegment.model_validate(
        {
            "id": "6e21df86-cad3-4de4-980d-8847328a7eed",
            "type": "flight",
            "title": {"values": [{"language": "en", "region": None, "value": "Azul 4056: Campinas to Manaus"}]},
            "description": {
                "values": [
                    {
                        "language": "en",
                        "region": None,
                        "value": "Economy (Y). Expedia itinerary: 73471665920059.",
                    }
                ]
            },
            "start_time_utc": "2026-07-14T16:00:00Z",
            "end_time_utc": "2026-07-14T19:50:00Z",
            "operator": {
                "name": {"values": [{"language": "en", "region": None, "value": "Azul"}]},
                "website": "https://www.voeazul.com.br/",
                "phone": None,
                "email": None,
            },
            "booking": {
                "provider": {
                    "name": {"values": [{"language": "en", "region": None, "value": "Expedia"}]},
                    "website": None,
                    "phone": "0330 123 1235",
                    "email": None,
                },
                "reference": "AEPL9L",
            },
            "start_place": {
                "name": {
                    "values": [
                        {
                            "language": "en",
                            "region": None,
                            "value": "Viracopos - Campinas International Airport",
                        }
                    ]
                },
                "country": "BR",
                "timezone": "America/Sao_Paulo",
                "coordinate": {"latitude": -23.0074, "longitude": -47.1345},
                "type": "airport",
                "iata_code": "VCP",
                "icao_code": "SBKP",
            },
            "end_place": {
                "name": {
                    "values": [{"language": "en", "region": None, "value": "Eduardo Gomes International Airport"}]
                },
                "country": "BR",
                "timezone": "America/Manaus",
                "coordinate": {"latitude": -3.0386, "longitude": -60.0497},
                "type": "airport",
                "iata_code": "MAO",
                "icao_code": "SBEG",
            },
            "flight_number": "AD4056",
        }
    ),
]
