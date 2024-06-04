from aiogram import Router

balance_dialog_router = Router()

balance_dialog_router.include_router(
    balance_dialog
)