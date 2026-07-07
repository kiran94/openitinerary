# OpenItinerary

OpenItinerary is an open, vendor-neutral standard for representing travel itineraries as structured data.

The goal is to create the equivalent of JSON for travel itineraries: a common, extensible specification that any travel company, airline, online travel agency, tour operator, booking platform, or application can produce and consume without relying on proprietary formats.

Rather than modelling every supplier independently, OpenItinerary models the underlying travel concepts. Every itinerary is composed of a sequence of strongly typed **Segments**, each representing an activity occurring over a period of time.

Examples include:

- Flights
- Trains
- Hotels
- Car rentals
- Airport transfers
- Public transport
- Tours

All segment types inherit from a common base model containing shared fields such as:

- Stable identifier
- Segment type
- Start and end timestamps (UTC-aware datetimes)
- Locations
- Supplier information
- Booking reference
- Status
- Metadata

Specialized segment types extend the base model with domain-specific fields while remaining compatible with generic itinerary consumers.

## Design Principles

- Vendor neutral
- Open standard
- JSON-first
- Language agnostic
- Schema driven
- Strongly typed
- Extensible through inheritance rather than arbitrary custom objects
- Backwards compatible through semantic versioning
- Canonical UTC timestamps (clients convert to local time for display)

## Data Modelling Principles

- Prefer explicit models over unstructured dictionaries.
- New concepts should be introduced as first-class schema types rather than "custom" extensions.
- Use inheritance to share common behaviour.
- Model real-world concepts instead of supplier-specific APIs.
- Every schema should be convertible into JSON Schema and consumable by multiple programming languages.

## Technology

The canonical schema is defined using Pydantic models (Python). JSON Schema is generated automatically from these models and acts as the portable interchange format. SDKs for other languages can be generated from the JSON Schema.

The repository is the canonical source of truth for the OpenItinerary specification.
