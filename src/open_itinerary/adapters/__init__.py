from abc import ABC, abstractmethod
from dataclasses import dataclass

from open_itinerary.models.segments import BaseSegment


@dataclass(frozen=True, slots=True)
class InputContent:
    data: bytes
    media_type: str  # e.g. "application/pdf", "text/html"


class Adapter(ABC):
    def load(self, content: InputContent) -> BaseSegment:
        temp = self._extract(content)
        return self._translate(temp)

    @abstractmethod
    def _extract(self, content: InputContent) -> str:
        pass

    @abstractmethod
    def _translate(self, content: str) -> BaseSegment:
        pass

    @abstractmethod
    def get_expected_media_types(self) -> set[str]:
        pass
