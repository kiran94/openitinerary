build:
	uv build

test:
	uv run --all-extras pytest

generate:
	PYTHONTZPATH="" uv run openitinerary schema --output stdout

generate_out:
	PYTHONTZPATH="" uv run openitinerary schema --output versioned --indent

format:
	uv run ruff check --fix
	uv run ruff format

api:
	uv run --all-extras fastapi dev src/openitinerary/adapters/api/main.py
