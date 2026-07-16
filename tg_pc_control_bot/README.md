# tg-pc-control-bot

Telegram-бот для мониторинга Windows-ПК с телефона.

## Возможности

- `/start` — главное меню
- Кнопка «Проверить статус» — CPU, RAM, Disk, Uptime, Network
- Доступ только для `OWNER_CHAT_ID`

## Структура

- `src/tg_pc_control_bot/main.py` — запуск
- `src/tg_pc_control_bot/bot/` — Telegram handlers и кнопки
- `src/tg_pc_control_bot/domain/use_cases/` — бизнес-логика
- `src/tg_pc_control_bot/infrastructure/` — работа с системой (psutil)
- `src/tg_pc_control_bot/security/` — проверка доступа

## Быстрый старт

1. Установить зависимости:
   ```bash
   pip install -r requirements.txt