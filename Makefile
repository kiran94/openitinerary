build:
	uv build

test:
	uv run --all-extras pytest

generate:
	PYTHONTZPATH="" uv run openitinerary --output stdout

generate_out:
	PYTHONTZPATH="" uv run openitinerary --output versioned --indent

visualise_schema: generate_out
	cd schemas/0.0 && uvx --from json-schema-for-humans generate-schema-doc itinerary.schema.json schema.html && open schema.html

format:
	uv run ruff check --fix
	uv run ruff format

api:
	uv run --all-extras fastapi dev src/openitinerary/adapters/api/main.py