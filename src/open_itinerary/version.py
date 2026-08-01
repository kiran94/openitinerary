import re

OPEN_ITINERARY_VERSION = "0.0.1"

semantic_version_regex = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def validate(version: str):
    if not semantic_version_regex.match(version):
        raise ValueError(f"{version} is not in the correct format. It must be a semantic version e.g 0.0.1")


def derive_major_minor(version: str) -> str:
    validate(version)

    p = semantic_version_regex.match(version)
    major = p.group(1)
    minor = p.group(2)

    return f"{major}.{minor}"


if __name__ == "__main__":
    print(derive_major_minor(OPEN_ITINERARY_VERSION))
