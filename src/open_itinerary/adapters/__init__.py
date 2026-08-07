from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import uuid4

from open_itinerary.models.itinerary import Segment


@dataclass(frozen=True, slots=True)
class InputContent:
    data: bytes
    media_type: str  # e.g. "application/pdf", "text/html"


class Adapter(ABC):
    def load(self, content: InputContent) -> list[Segment]:
        temp = self._extract(content)
        temp = self._translate(temp)
        temp = self._post_process(temp)
        return temp

    @abstractmethod
    def _extract(self, content: InputContent) -> str:
        pass

    @abstractmethod
    def _translate(self, content: str) -> list[Segment]:
        pass

    @abstractmethod
    def get_expected_media_types(self) -> set[str]:
        pass

    def _post_process(self, segments: list[Segment]) -> list[Segment]:
        for segment in segments:
            segment.id = uuid4()

        return segments
