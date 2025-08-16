from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Optional
from .config import settings


class MemoryStore:
    def __init__(self, db_path: Optional[Path] = None) -> None:
        self.db_path = db_path or settings.data_dir / "memory.sqlite3"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self.db_path))
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._conn.execute("PRAGMA synchronous=NORMAL;")
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self._conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS docs (
                id INTEGER PRIMARY KEY,
                url TEXT,
                title TEXT,
                source TEXT,
                tags TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                text TEXT
            );
            """
        )
        cur.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts
            USING fts5(title, text, url, content='');
            """
        )
        self._conn.commit()

    def add_document(
        self,
        *,
        url: str | None,
        title: str | None,
        text: str,
        source: str = "web",
        tags: str | None = None,
    ) -> int:
        cur = self._conn.cursor()
        cur.execute(
            "INSERT INTO docs(url, title, source, tags, text) VALUES (?, ?, ?, ?, ?)",
            (url, title, source, tags, text),
        )
        doc_id = cur.lastrowid
        # Insert to FTS (contentless)
        cur.execute(
            "INSERT INTO docs_fts(rowid, title, text, url) VALUES (?, ?, ?, ?)",
            (doc_id, title or "", text, url or ""),
        )
        self._conn.commit()
        return int(doc_id)

    def bulk_add(self, docs: Iterable[dict]) -> list[int]:
        ids: list[int] = []
        for d in docs:
            ids.append(
                self.add_document(
                    url=d.get("url"),
                    title=d.get("title"),
                    text=d.get("text", ""),
                    source=d.get("source", "web"),
                    tags=d.get("tags"),
                )
            )
        return ids

    def search(self, query: str, limit: int = 10) -> list[dict]:
        cur = self._conn.cursor()
        cur.execute(
            """
            SELECT d.id, d.url, d.title,
                   snippet(docs_fts, 1, '[', ']', ' … ', 10) as snippet
            FROM docs_fts
            JOIN docs d ON d.id = docs_fts.rowid
            WHERE docs_fts MATCH ?
            ORDER BY bm25(docs_fts)
            LIMIT ?
            """,
            (query, int(limit)),
        )
        rows = cur.fetchall()
        return [
            {"id": r[0], "url": r[1], "title": r[2], "snippet": r[3]}
            for r in rows
        ]

    def get(self, doc_id: int) -> dict | None:
        cur = self._conn.cursor()
        cur.execute(
            "SELECT id, url, title, source, tags, created_at, text FROM docs WHERE id = ?",
            (int(doc_id),),
        )
        row = cur.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "url": row[1],
            "title": row[2],
            "source": row[3],
            "tags": row[4],
            "created_at": row[5],
            "text": row[6],
        }

    def close(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass


store = MemoryStore()