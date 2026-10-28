import pytest

from openitinerary import generate_schema
from openitinerary.version import (
    JSON_SCHEMA_DIALECT,
    OPEN_ITINERARY_SCHEMA_URL,
    derive_major_minor,
    validate,
)


def test_generated_schema_declares_dialect_and_canonical_id():
    schema = generate_schema()

    assert schema["$schema"] == JSON_SCHEMA_DIALECT
    assert schema["$id"] == OPEN_ITINERARY_SCHEMA_URL


@pytest.mark.parametrize(
    "input",
    [
        ("0.0.0.1"),
        ("version1"),
        ("goofy"),
        ("01.2.3"),
        ("1.02.3"),
        ("1.2.03"),
        ("1.2.3-01"),
        ("1.2.3-rc..1"),
        ("1.2.3+build..4"),
        ("١.2.3"),
    ],
)
def test_validate_invalid(input: str):
    with pytest.raises(ValueError, match="not in the correct format"):
        validate(input)


@pytest.mark.parametrize(
    "input",
    [
        ("0.0.1"),
        ("1.0.1"),
        ("2.0.3"),
        ("1.2.3-rc.1"),
        ("1.2.3+build.4"),
        ("1.2.3-rc.1+build.4"),
    ],
)
def test_validate_valid(input: str):
    validate(input)


@pytest.mark.parametrize(
    "input,expected",
    [
        ("0.1.0", "0.1"),
        ("1.0.0", "1.0"),
        ("1.5.0", "1.5"),
        ("10.0.0", "10.0"),
        ("1.2.3-rc.1", "1.2"),
        ("1.2.3+build.4", "1.2"),
    ],
)
def test_derive_major_minor(input: str, expected: str):
    actual = derive_major_minor(input)
    assert actual == expected
