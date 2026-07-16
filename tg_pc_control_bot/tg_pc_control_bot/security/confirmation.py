from __future__ import annotations

import secrets
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class PendingConfirmation:
    token: str
    chat_id: int
    command_name: str
    expires_at: float


class ConfirmationService:
    def __init__(self, ttl_seconds: int) -> None:
        self._ttl_seconds = ttl_seconds
        self._pending_by_chat: dict[int, PendingConfirmation] = {}

    def create(self, chat_id: int, command_name: str) -> PendingConfirmation:
        token = secrets.token_urlsafe(16)
        pending = PendingConfirmation(
            token=token,
            chat_id=chat_id,
            command_name=command_name,
            expires_at=time.monotonic() + self._ttl_seconds,
        )
        self._pending_by_chat[chat_id] = pending
        return pending

    def consume(self, chat_id: int, token: str, command_name: str) -> bool:
        pending = self._pending_by_chat.get(chat_id)
        if pending is None:
            return False
        if pending.expires_at < time.monotonic():
            self._pending_by_chat.pop(chat_id, None)
            return False
        if pending.token != token or pending.command_name != command_name:
            return False
        self._pending_by_chat.pop(chat_id, None)
        return True

    def clear(self, chat_id: int) -> None:
        self._pending_by_chat.pop(chat_id, None)
