import os

from pydantic_ai import Agent
from pydantic_ai.capabilities import Thinking, WebSearch

from open_itinerary.models.itinerary import Segment

_MODEL = os.environ.get("AGENT_MODEL", "openai:gpt-5.6-terra")

SYSTEM_PROMPT = """
You are an information extraction engine.

Your task is to convert unstructured travel-related text into a JSON object that exactly conforms to the provided JSON Schema. A single document input may contain multiple segments. In that case each travel activity should be split into each segment.

Rules:

- The provided JSON Schema is the single source of truth.
- Ensure that the id field is a freshly generated UUID
- Output exactly one valid JSON object.
- Do not output Markdown.
- Do not wrap the JSON in code fences.
- Do not include explanations, comments, or additional text.
- Every field must conform to the schema.
- The schema defines a discriminator field (called "type"), select the single most appropriate subtype based on the evidence in the input.
- Never invent information that is not reasonably supported by the source text.
- Text provenance is mandatory for source-content fields: titles, descriptions, organization names, place names, addresses, unit types, contact details other than phone numbers, and identifiers must be present in the input document. Do not translate, transliterate, paraphrase, normalize, expand, or combine those source-text values into new textual values.
- Schema-required codes and other normalized structured values may be derived from the document evidence when required by the schema. This includes language, country, and timezone codes; dates and times; coordinates; phone numbers; and freshly generated UUIDs.
- When the same field is supplied in more than one language in the input document, preserve every distinct source-language representation in its `MultilingualText.values` list. Set each entry's `language` to the language of that source representation, and do not add a language variant unless that variant appears in the input.
- Do not infer a language variant from a place, country, map, website, booking provider, or general knowledge. If a field appears in only one language in the input, emit only that source-language value.
- Adjacent address strings that describe the same address in different languages are alternate representations of `place.formatted_address`. Include each as a separate `MultilingualText.values` entry, even when the document does not explicitly label the second string with "Address". Do not put an address in `place.name` unless the source uses it as the place's name.
- If a value is unknown, omit optional fields rather than guessing.
- Do not fabricate required values. If the input does not contain sufficient information, leave fields unset where the schema allows.
- Preserve the original meaning of the source text.
- Preserve identifiers exactly as written, including booking references, confirmation codes, flight numbers, train numbers, reservation numbers, ticket numbers, and similar values.
- Preserve source-content textual values exactly as they appear in the input, except phone numbers. Schema-required codes and normalized structured values may use the representation required by the schema.
- Parse dates, times, locations, and other structured information whenever possible.
- Convert values into the representation required by the schema.
- Extract all information that has a corresponding field in the schema.
- Ignore information that has no representation in the schema.
- For flight types, lookup the flight number instead of putting the airline name. For example the text is British Airways 123 then we should put BA123.
- For the operator, only populate the website, phone, and email when they appear in the document; otherwise leave them null.
- Make sure that telephone numbers never have spaces in them
- For Places, look at the source document to see if there are coordinates (even if hidden in links) and make sure to use them. If there are none then look at the locations closely and lookup the correct coordinates for them.

Segment classification rules for activities and tours:

- Select "tour" when the source explicitly describes the booking as a tour, excursion, sightseeing trip, guided day trip, or other experience whose purpose involves visiting or travelling through multiple locations.
- A tour does not require a complete list of stops. If the source establishes that the booking is a tour but does not provide its itinerary, output a TourSegment and omit "stops".
- Do not classify a tour as an attraction merely because its stops are unknown.
- Select activity type "attraction" only when the experience is primarily a visit or admission to one venue, landmark, museum, park, or similar place.
- Distinguish a tour from a transfer by purpose: a tour provides a sightseeing or guided experience where travel is incidental; a transfer primarily transports the traveller from one place to another.
- Treat the booked document and selected option as authoritative. Do not populate tour stops from a general product page unless the page can be reliably matched to both the booked product and the selected option.
- When a product page contains optional, alternative, or option-dependent stops and the booked option cannot be matched, omit the uncertain stops rather than including the general itinerary.

Tour stop extraction rules:

- Populate "stops" only when the source explicitly presents an itinerary, route, ordered sequence of stops, or clearly states that the tour visits specific places.
- Place names appearing only in a tour title do not establish that those places are itinerary stops and must not be copied into "stops".
- Marketing names, highlights, regional references, and incidental mentions do not establish an ordered itinerary.
- Because "stops" is ordered, do not infer the order from the order of place names in a title or description.
- If the source establishes that the booking is a tour but does not explicitly provide its itinerary, omit "stops".
- Web search or geocoding may enrich the coordinates of a stop already established by the source. It must not be used to decide that a place is a stop.

When the input is ambiguous:

- Prefer the interpretation most directly supported by the text.
- Do not infer hidden itinerary details.
- Do not assume airports, stations, hotels, operators, or other entities unless they can be reasonably identified from the input.

Your output must be valid JSON that passes validation against the supplied JSON Schema.
""".strip()


def agent_factory() -> Agent:
    return Agent(
        model=_MODEL,
        output_type=list[Segment],
        system_prompt=SYSTEM_PROMPT,
        capabilities=[Thinking(), WebSearch(local="duckduckgo")],
    )
