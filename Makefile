build:
	uv build

test:
	uv run --all-extras pytest

generate:
	PYTHONTZPATH="" uv run open-itinerary --output stdout

generate_out:
	PYTHONTZPATH="" uv run open-itinerary --output versioned --indent

visualise_schema: generate_out
	cd schemas/0.0 && uvx --from json-schema-for-humans generate-schema-doc itinerary.schema.json schema.html && open schema.html

format:
	uv run ruff check --fix
	uv run ruff format

api:
	uv run --all-extras fastapi dev src/open_itinerary/adapters/api/main.py