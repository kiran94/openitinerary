import json
import os
from glob import glob
from pathlib import Path

import pytest
from jsonschema.validators import validator_for

from openitinerary.models.itinerary import Itinerary

_examples_folder = Path(os.getcwd()) / "examples"
_schema_file = Path(os.getcwd()) / "schemas" / "0.1" / "itinerary.schema.json"
_schema = json.loads(_schema_file.read_text(encoding="utf-8"))
_validator_class = validator_for(_schema)
_validator_class.check_schema(_schema)
_validator = _validator_class(_schema)


@pytest.mark.parametrize("file", glob("*.json", root_dir=_examples_folder))
def test_validate_examples(file: str):
    with open(_examples_folder / file, "r", encoding="utf-8") as f:
        document = json.load(f)

    _validator.validate(document)
    Itinerary.model_validate(document)
