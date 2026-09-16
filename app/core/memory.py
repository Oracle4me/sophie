from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel
from app.core.models import MemoryCandidate


class MemoryRecord(BaseModel):
    """
    Satu unit memory Sophie.

    Untuk v0.4, memory masih sederhana dan disimpan
    sebagai data terstruktur.
    """

    content: str
    memory_type: str = "semantic"
    importance: float = 0.5
    created_at: datetime

class MemoryPolicy:
    """
    Menentukan apakah sebuah informasi layak disimpan
    sebagai memory Sophie.

    v0.4.1 menggunakan aturan eksplisit sederhana.
    """

    MIN_IMPORTANCE = 0.6

    def evaluate(
        self,
        content: str,
        memory_type: str = "semantic",
        importance: float = 0.5,
    ) -> MemoryCandidate:
        should_store = (
            bool(content.strip())
            and 0.0 <= importance <= 1.0
            and importance >= self.MIN_IMPORTANCE
        )

        return MemoryCandidate(
            content=content,
            memory_type=memory_type,
            importance=importance,
            should_store=should_store,
        )

class MemoryStore:
    """
    Penyimpanan memory lokal Sophie.

    v0.4 menggunakan JSON sederhana.
    Database akan ditambahkan pada tahap berikutnya.
    """

    def __init__(self, file_path: str = "data/memories.json") -> None:
        self.file_path = Path(file_path)
        self.memories: list[MemoryRecord] = []

        self._load()

    def add(
        self,
        content: str,
        memory_type: str = "semantic",
        importance: float = 0.5,
    ) -> MemoryRecord:
        memory = MemoryRecord(
            content=content,
            memory_type=memory_type,
            importance=importance,
            created_at=datetime.now(timezone.utc),
        )

        self.memories.append(memory)
        self._save()

        return memory

    def save_if_allowed(self, candidate: MemoryCandidate,) -> MemoryRecord | None:
        """
            Menyimpan memory hanya jika MemoryPolicy
            menyatakan candidate layak disimpan.
        """
        if not candidate.should_store:
            return None

        return self.add(
            content=candidate.content,
            memory_type=candidate.memory_type,
            importance=candidate.importance,
        )

    def get_all(self) -> list[MemoryRecord]:
        return list(self.memories)

    def clear(self) -> None:
        self.memories.clear()
        self._save()

    def _load(self) -> None:
        if not self.file_path.exists():
            return

        import json

        data = json.loads(
            self.file_path.read_text(encoding="utf-8")
        )

        self.memories = [
            MemoryRecord.model_validate(item)
            for item in data
        ]

    def _save(self) -> None:
        import json

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.file_path.write_text(
            json.dumps(
                [
                    memory.model_dump(mode="json")
                    for memory in self.memories
                ],
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
