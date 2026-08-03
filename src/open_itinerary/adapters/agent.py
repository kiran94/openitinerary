import os
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.capabilities import Thinking, WebSearch

from open_itinerary.adapters import SYSTEM_PROMPT
from open_itinerary.models.itinerary import Segment

_MODEL = os.environ.get("AGENT_MODEL", "openai:gpt-5.6-terra")


def agent_factory() -> Agent:
    return Agent(
        model=_MODEL,
        output_type=list[Segment],
        system_prompt=SYSTEM_PROMPT,
        capabilities=[Thinking(), WebSearch(local="duckduckgo")],
        model_settings=ModelSettings(temperature=0.0),
    )
