"""
config.py — настройки приложения.

"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"


@dataclass(frozen=True)
class AppConfig:
    
    bot_token: str
    owner_chat_ids: tuple[int, ...]
    log_level: str


def load_config() -> AppConfig:
    
    load_dotenv(ENV_PATH)

    bot_token = os.getenv("BOT_TOKEN", "").strip()
    owner_raw = os.getenv("OWNER_CHAT_ID", "").strip()
    log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper()

    if not bot_token:
        raise ValueError("BOT_TOKEN не задан. Проверь файл .env")
    if not owner_raw:
        raise ValueError("OWNER_CHAT_ID не задан. Проверь файл .env")

    
    owner_chat_ids = tuple(int(part.strip()) for part in owner_raw.split(",") if part.strip())

    return AppConfig(
        bot_token=bot_token,
        owner_chat_ids=owner_chat_ids,
        log_level=log_level,
    )