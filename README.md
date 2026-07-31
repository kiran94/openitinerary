# OpenItinerary

OpenItinerary is an open, vendor-neutral standard for representing travel itineraries as structured data.

Create the equivalent of JSON for travel itineraries to facilitate a common specification that any travel company can produce or consume without relying on proprietary formats. A single itinerary can contain flights, trains, accommodation and other travel related activities from various vendors within a single unified model.

Principles:
* Vendor Neutral: No dependency on any particular vendor proprietary format. Instead model the underlying travel concepts.
* Open & Interoperable: Designed to move cleanly between systems and programming languages.
* Strongly Typed: Fields have clear semantics and avoid ambiguity. Missing concept and fields should be proposed to be added to the standard and there should be no custom metadata "escape hatches".
* Minimal: Universal Concepts are defined at the base models and domain specifics belong in specialized types.
* Serialization Friendly: Data model will at *minimum* map cleanly to JSON.
* Versioning: Schema is versioned and follows standard semantic versioning rules.
* Single Canonical Time: Date/Times are *always* stored in UTC format. Geographic Places will always store the Time zone in which they take place. Downstream applications are responsible for ensuring that time presented correctly.
* Internationalization: International differences are handled explicitly. Textual fields will store the language they are stored in so that downstream applications can present/provide translation when needed.


## Implementation

The schema is defined and maintained using *Pydantic Models* however this does not mean that OpenItinerary is a python project. These models are used to generate a **JSON Schema** which serves as the canonical schema of the project.

JSON is the default interchange format because it is universal, readable, and easy to integrate. From this format, other formats can be derived:

```mermaid
graph LR

Pydantic(Pydantic Models)
JSONSchema(JSON Schema)

Pydantic --> JSONSchema

JSONSchema --> Typescript
JSONSchema --> Protobuf
JSONSchema --> Flatbuffer
JSONSchema --> ...
```

*Performance sensitive consumers may want to use binary formats such as Protobuf so the standard only states that JSON is a minimum supported format. Binary formats must represent the same model.*

## Concepts

* `Itinerary`: An itinerary is an ordered collection of typed segments.
* `Segment`: A travel activity that happens at a specified time at a specific place.
* `Place`: A geographical location on the earth.

The `BaseSegment` defined common concepts for all travel related activities and domain specific models such as `FlightSegment` add stronger fields and validation.