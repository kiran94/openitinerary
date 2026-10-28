import argparse
import json
import logging
import os
from pathlib import Path

from openitinerary.models.itinerary import Itinerary
from openitinerary.version import (
    JSON_SCHEMA_DIALECT,
    OPEN_ITINERARY_SCHEMA_URL,
    OPEN_ITINERARY_VERSION,
    derive_major_minor,
)

logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

SCHEMAS_FOLDER = "schemas"
SCHEMAS_FILE = "itinerary.schema.json"


def generate_schema() -> dict:
    return {
        "$schema": JSON_SCHEMA_DIALECT,
        "$id": OPEN_ITINERARY_SCHEMA_URL,
        **Itinerary.model_json_schema(),
    }


def _handle_schema_command(args: argparse.Namespace) -> None:
    def _schema(output: str, indent: bool):
        logger.debug("generating schema from Itinerary")
        schema = generate_schema()

        indent_val = 4 if indent else None

        if output == "stdout":
            print(json.dumps(schema, indent=indent_val))
        elif output == "versioned":
            major_minor_folder = derive_major_minor(OPEN_ITINERARY_VERSION)
            versioned_folder = Path(os.getcwd()) / SCHEMAS_FOLDER / major_minor_folder
            versioned_file = versioned_folder / SCHEMAS_FILE

            logger.info("output schema to %s", versioned_file)

            os.makedirs(versioned_folder, exist_ok=True)

            with open(versioned_file, "w") as f:
                json.dump(schema, f, indent=indent_val)
        else:
            raise NotImplementedError(f"unknown output: {output}")

    _schema(args.output, args.indent)


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    schema_parser = subparsers.add_parser("schema", help="generate an openitinerary schema")
    schema_parser.add_argument("-o", "--output", choices=["stdout", "versioned"], default="stdout")
    schema_parser.add_argument("-i", "--indent", action="store_true")
    schema_parser.set_defaults(handler=_handle_schema_command)

    args = parser.parse_args()
    args.handler(args)
