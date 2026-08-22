import os
from pathlib import Path

from openitinerary.models.itinerary import Itinerary


def test_validate_examples():
    examples_folder = Path(os.getcwd()) / "examples"
    target_files = []

    for file in os.listdir(examples_folder):
        if file.endswith(".json"):
            target_files.append(examples_folder / file)

    for target in target_files:
        with open(target, "r") as f:
            Itinerary.model_validate_json(f.read())
