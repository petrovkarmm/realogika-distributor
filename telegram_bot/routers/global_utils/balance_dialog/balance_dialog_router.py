from aiogram import Router

from routers.global_utils.balance_dialog.balance_dialog import balance_dialog

balance_dialog_router = Router()

balance_dialog_router.include_router(
    balance_dialog
)
