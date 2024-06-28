from aiogram import Router

from telegram_bot.routers.ref_program.balance_dialog.balance_dialog import shop_dialog

shop_dialog_router = Router()

shop_dialog_router.include_router(
    shop_dialog
)
