

build:
	uv build

generate:
	uv run open-itinerary | jq | bat -l json

