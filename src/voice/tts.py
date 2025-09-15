from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Tuple
from xml.etree import ElementTree as ET


@dataclass
class TTSRequest:
    text: str
    voice: str | None = None
    style: str | None = None
    ssml: bool = False


@dataclass
class TTSChunk:
    data: bytes
    seq: int
    final: bool


class BaseTTSAdapter(ABC):
    @abstractmethod
    def synthesize_stream(self, req: TTSRequest) -> Iterable[TTSChunk]:
        ...

    @abstractmethod
    def supports_ssml(self) -> bool:
        ...


def parse_ssml(text: str) -> Tuple[str, Dict[str, Any]]:
    """Parse minimal SSML and return plain text and extracted controls.

    Recognizes ``<prosody rate>``, ``<emphasis level>`` and ``<break time>``.
    Unknown tags are ignored. Returns the text content with tags removed and a
    dictionary of parsed controls.
    """
    controls: Dict[str, Any] = {}
    try:
        root = ET.fromstring(f"<root>{text}</root>")
    except ET.ParseError:
        return text, controls

    parts: list[str] = []
    for elem in root.iter():
        if elem.tag == "prosody":
            rate = elem.attrib.get("rate")
            if rate:
                controls["prosody.rate"] = rate
        elif elem.tag == "emphasis":
            level = elem.attrib.get("level")
            if level:
                controls["emphasis.level"] = level
        elif elem.tag == "break":
            time = elem.attrib.get("time")
            if time and time.endswith("ms"):
                try:
                    controls["break.ms"] = int(time[:-2])
                except ValueError:
                    pass
        if elem.text:
            parts.append(elem.text)
        if elem.tail:
            parts.append(elem.tail)

    plain = "".join(parts).strip()
    return plain, controls
