from aiogram import Router

from routers.global_utils.message_thread.message_thread_dialog import message_thread_dialog

message_thread_router = Router()

message_thread_router.include_router(
    message_thread_dialog
)
