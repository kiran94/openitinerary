from abc import ABC, abstractmethod
from dataclasses import dataclass

from opentelemetry import trace

from openitinerary.models.itinerary import Segment


class DocumentExtractionError(ValueError):
    """Raised when declared document content cannot be extracted."""


@dataclass(frozen=True, slots=True)
class InputContent:
    data: bytes
    media_type: str  # e.g. "application/pdf", "text/html"


class Adapter(ABC):
    async def load(self, content: InputContent) -> list[Segment]:
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("Adapter Extract", attributes={"content.length.bytes": len(content.data)}):
            temp = await self._extract(content)

        with tracer.start_as_current_span("Adapter Translate", attributes={"extracted.length.string": len(temp)}):
            segments = await self._translate(temp)

        return segments

    @abstractmethod
    async def _extract(self, content: InputContent) -> str:
        """
        Takes the input content and translates it into common string.
        """

    @abstractmethod
    async def _translate(self, content: str) -> list[Segment]:
        """
        Takes the input string and transcribe into structured list of
        Segments.
        """

    @abstractmethod
    def get_expected_media_types(self) -> set[str]:
        """
        Declares the expected media types that this adapter supports
        """

    def check_media_type(self, content: InputContent) -> None:
        expected_media_type = self.get_expected_media_types()
        if content.media_type not in expected_media_type:
            raise ValueError(
                f"{content.media_type} is not supported by this adapter. Expected {','.join(expected_media_type)}"
            )
