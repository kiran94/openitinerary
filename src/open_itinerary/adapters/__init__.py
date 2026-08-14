from abc import ABC, abstractmethod
from dataclasses import dataclass

from open_itinerary.models.itinerary import Segment


class DocumentExtractionError(ValueError):
    """Raised when declared document content cannot be extracted."""


@dataclass(frozen=True, slots=True)
class InputContent:
    data: bytes
    media_type: str  # e.g. "application/pdf", "text/html"


class Adapter(ABC):
    async def load(self, content: InputContent) -> list[Segment]:
        temp = await self._extract(content)
        return await self._translate(temp)

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
