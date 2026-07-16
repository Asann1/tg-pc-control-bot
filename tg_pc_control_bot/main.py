"""
main.py — точка входа.

"""

from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from tg_pc_control_bot.bot.handlers import BotHandlers
from tg_pc_control_bot.config import load_config
from tg_pc_control_bot.domain.use_cases.get_status import GetStatusUseCase
from tg_pc_control_bot.infrastructure.metrics.psutil_metrics import PsutilMetricsGateway
from tg_pc_control_bot.observability.logging import configure_logging
from tg_pc_control_bot.security.policies import AuthPolicy


def build_application() -> Application:
    # Настройки
    config = load_config()
    configure_logging(config.log_level)

    # Зависимости (снизу вверх: metrics -> use case -> handlers)
    auth_policy = AuthPolicy(owner_chat_ids=config.owner_chat_ids)
    metrics_gateway = PsutilMetricsGateway()
    get_status_use_case = GetStatusUseCase(metrics_gateway)
    handlers = BotHandlers(auth_policy=auth_policy, get_status_use_case=get_status_use_case)

    # Telegram Application
    application = Application.builder().token(config.bot_token).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(
        CallbackQueryHandler(handlers.status_callback, pattern="^status:check$")
    )
    application.add_handler(
        CallbackQueryHandler(handlers.back_to_menu_callback, pattern="^menu:back$")
    )

    return application


def main() -> None:
    application = build_application()
    print("Бот запущен. Остановка: Ctrl+C")
    application.run_polling()


if __name__ == "__main__":
    main()