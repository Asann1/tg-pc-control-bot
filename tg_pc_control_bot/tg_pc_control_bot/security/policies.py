from __future__ import annotations

import time
from collections import defaultdict

from tg_pc_control_bot.domain.commands import CommandScope


class AuthPolicy:
    def __init__(self, owner_chat_ids: tuple[int, ...]) -> None:
        self._owner_chat_ids = set(owner_chat_ids)

    def is_allowed(self, chat_id: int, _scope: CommandScope) -> bool:
        return chat_id in self._owner_chat_ids


class CooldownPolicy:
    def __init__(self, cooldown_seconds: int) -> None:
        self._cooldown_seconds = cooldown_seconds
        self._last_used: dict[tuple[int, str], float] = defaultdict(float)

    def check(self, chat_id: int, command_name: str) -> tuple[bool, int]:
        if self._cooldown_seconds == 0:
            return True, 0
        now = time.monotonic()
        key = (chat_id, command_name)
        diff = now - self._last_used[key]
        if diff < self._cooldown_seconds:
            wait_seconds = int(self._cooldown_seconds - diff) + 1
            return False, wait_seconds
        self._last_used[key] = now
        return True, 0
