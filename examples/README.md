# OpenItinerary Examples

These synthetic itineraries demonstrate different parts of the OpenItinerary
model. Every JSON document is validated against the current Python model by the
automated test suite.

All travellers, booking references, and record locators are fictional. Real
organizations, routes, and places are used where they make an example easier
to understand.

## Choose an example

| Example | Purpose |
| --- | --- |
| [`minimal-flight.json`](minimal-flight.json) | The smallest introduction to OpenItinerary: a single flight segment with an operator, airports, UTC times, and local time zones. Start here when evaluating the format or following the root README's Quick Start. |
| [`multi-provider-trip.json`](multi-provider-trip.json) | A broad, real-world composition spanning Singapore, Beijing, and Xi'an. It combines flights, a taxi transfer, two hotel stays, high-speed rail, and four tours booked through several providers. English and Simplified Chinese values demonstrate localization within a larger itinerary. |
| [`multilingual-trip.json`](multilingual-trip.json) | A focused localization example using English and Japanese across flight, train, accommodation, and activity segments. Use it when implementing locale selection or checking how translated values coexist with canonical UTC times and IANA time zones. |

## Validation

From the repository root, validate every example with the project test suite:

```bash
make test
```

The parameterized example test discovers each JSON file in this directory and
constructs an `Itinerary` from it. A document that no longer matches the model
causes the test suite to fail.
