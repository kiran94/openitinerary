import os
import json
import logging
import argparse
from pathlib import Path

from open_itinerary.models.itinerary import Itinerary
from open_itinerary.version import OPEN_ITINERARY_VERSION, derive_major_minor

logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

SCHEMAS_FOLDER = "schemas"
SCHEMAS_FILE = "itinerary.schema.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", choices=["stdout", "versioned"], default="stdout")
    parser.add_argument("-i", "--indent", action="store_true")

    args = parser.parse_args()

    logger.debug("generating schema from Itinerary")
    schema = Itinerary.model_json_schema()

    indent = 4 if args.indent else None

    if args.output == "stdout":
        print(json.dumps(schema, indent=indent))
    elif args.output == "versioned":
        major_minor_folder = derive_major_minor(OPEN_ITINERARY_VERSION)
        versioned_folder = Path(os.getcwd()) / SCHEMAS_FOLDER / major_minor_folder
        versioned_file = versioned_folder / SCHEMAS_FILE

        logger.info("output schema to %s", versioned_file)

        os.makedirs(versioned_folder, exist_ok=True)

        with open(versioned_file, "w") as f:
            json.dump(schema, f, indent=indent)
    else:
        raise NotImplementedError({args.output})
