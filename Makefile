build:
	uv build

test:
	uv run pytest

generate:
	uv run open-itinerary --output stdout

generate_out:
	uv run open-itinerary --output versioned --indent

visualise_schema: generate_out
	cd schemas/0.0.1 && uvx --from json-schema-for-humans generate-schema-doc schema.json schema.html && open schema.html
