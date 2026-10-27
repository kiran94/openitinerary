import os
from glob import glob
from pathlib import Path

import pytest

from openitinerary.models.itinerary import Itinerary

_examples_folder = Path(os.getcwd()) / "examples"


@pytest.mark.parametrize("file", glob("*.json", root_dir=_examples_folder))
def test_validate_examples(file: str):
    with open(_examples_folder / file, "r", encoding="utf-8") as f:
        Itinerary.model_validate_json(f.read())
