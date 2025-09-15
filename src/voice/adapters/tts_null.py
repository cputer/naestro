from __future__ import annotations

from typing import Iterable

from ..tts import BaseTTSAdapter, TTSChunk, TTSRequest, parse_ssml


class NullTTSAdapter(BaseTTSAdapter):
    def supports_ssml(self) -> bool:
        return True

    def synthesize_stream(self, req: TTSRequest) -> Iterable[TTSChunk]:
        text = req.text
        if req.ssml:
            text, _ = parse_ssml(text)
        data = text.encode()
        num_chunks = min(5, max(3, (len(data) + 99) // 100))
        chunk_size = max(1, (len(data) + num_chunks - 1) // num_chunks)
        seq = 0
        for i in range(0, len(data), chunk_size):
            end = i + chunk_size
            final = end >= len(data)
            yield TTSChunk(data=data[i:end], seq=seq, final=final)
            seq += 1
