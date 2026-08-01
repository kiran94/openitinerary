import re


OPEN_ITINERARY_VERSION = "0.0.1"
"""
Version of the published OpenItinerary Schema.

This is conceptually different to the version defined in pyproject.toml
of this project because the version of the python package may include
implementation-only work such as tooling improvements, documentation changes etc
which may not result in a new published schema.
"""

semantic_version_regex = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def validate(version: str):
    if not semantic_version_regex.match(version):
        raise ValueError(
            f"{version} is not in the correct format. It must be a semantic version e.g 0.0.1 ({semantic_version_regex.pattern})"
        )


def derive_major_minor(version: str) -> str:
    validate(version)

    p = semantic_version_regex.match(version)
    major = p.group(1)
    minor = p.group(2)

    return f"{major}.{minor}"


if __name__ == "__main__":
    print(derive_major_minor(OPEN_ITINERARY_VERSION))
