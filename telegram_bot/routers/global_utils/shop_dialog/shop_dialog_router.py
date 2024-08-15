from aiogram import Router

from routers.global_utils.shop_dialog.shop_dialog import shop_dialog

shop_dialog_router = Router()


shop_dialog_router.include_router(
    shop_dialog
)
