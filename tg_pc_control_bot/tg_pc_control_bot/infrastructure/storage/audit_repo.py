from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class AuditEvent:
    chat_id: int
    command_name: str
    scope: str
    success: bool
    details: str


class AuditRepository:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp_utc TEXT NOT NULL,
                    chat_id INTEGER NOT NULL,
                    command_name TEXT NOT NULL,
                    scope TEXT NOT NULL,
                    success INTEGER NOT NULL,
                    details TEXT NOT NULL
                );
                """
            )

    def append(self, event: AuditEvent) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO audit_events (timestamp_utc, chat_id, command_name, scope, success, details)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    datetime.now(tz=timezone.utc).isoformat(),
                    event.chat_id,
                    event.command_name,
                    event.scope,
                    int(event.success),
                    event.details,
                ),
            )
