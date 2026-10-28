import json
import os
from glob import glob
from pathlib import Path

import pytest
from jsonschema.protocols import Validator
from jsonschema.validators import validator_for

from openitinerary import SCHEMAS_FILE, SCHEMAS_FOLDER
from openitinerary.models.itinerary import Itinerary
from openitinerary.version import OPEN_ITINERARY_VERSION, derive_major_minor

_examples_folder = Path(os.getcwd()) / "examples"


@pytest.fixture(scope="module")
def validator() -> Validator:
    _schema_file = Path(os.getcwd()) / SCHEMAS_FOLDER / derive_major_minor(OPEN_ITINERARY_VERSION) / SCHEMAS_FILE
    _schema = json.loads(_schema_file.read_text(encoding="utf-8"))
    _validator_class = validator_for(_schema)
    _validator_class.check_schema(_schema)
    return _validator_class(_schema)


@pytest.mark.parametrize("file", glob("*.json", root_dir=_examples_folder))
def test_validate_examples(file: str, validator: Validator):
    with open(_examples_folder / file, "r", encoding="utf-8") as f:
        document = json.load(f)

    validator.validate(document)
    Itinerary.model_validate(document)
