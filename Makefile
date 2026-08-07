build:
	uv build

test:
	uv run --all-extras pytest

generate:
	uv run open-itinerary --output stdout

generate_out:
	uv run open-itinerary --output versioned --indent

visualise_schema: generate_out
	cd schemas/0.0 && uvx --from json-schema-for-humans generate-schema-doc itinerary.schema.json schema.html && open schema.html
