

build:
	uv build

generate:
	uv run open-itinerary | jq | bat -l json

generate_out:
	cd schemas && uv run --project .. open-itinerary > schema.json.tmp && jq . schema.json.tmp > schema.json && rm schema.json.tmp

visualise_schema: generate_out
	cd schemas && uvx --from json-schema-for-humans generate-schema-doc schema.json schema.html && open schema.html
