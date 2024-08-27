import calendar
from pprint import pprint
from typing import Any, Dict
from aiogram import F, Bot
from aiogram.methods import Close
from aiogram_dialog import Dialog, Window, DialogManager, SubManager
from aiogram_dialog.widgets.kbd import (
    Button, ListGroup,
    Row, Radio,
    Checkbox, ManagedCheckbox, StubScroll, NumberedPager, Cancel
)
from aiogram_dialog.widgets.media import DynamicMedia, StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from routers.global_utils.message_thread.message_thread_states import MessageThreadStates

ID_STUB_SCROLL = "stub_scroll"


def when_checked(data: Dict, widget, manager: SubManager) -> bool:
    # manager for our case is already adapted for current ListGroup row
    # so `.find` returns widget adapted for current row
    # if you need to find widgets outside the row, use `.find_in_parent`
    check: ManagedCheckbox = manager.find("check")
    return check.is_checked()


async def data_getter(*args, **kwargs):
    return {
        "fruits": ["mango", "papaya", "kiwi"],
        "colors": ["blue", "pink"],
    }


message_thread_main_menu_window = Window(
    Const(
        "Hello, please check you options for each item:",
    ),
    ListGroup(
        Checkbox(
            Format("✓ {item}"),
            Format("  {item}"),
            id="check",
        ),
        Row(
            Radio(
                Format("🔘 {item} ({data[item]})"),
                Format("⚪️ {item} ({data[item]})"),
                id="radio",
                item_id_getter=str,
                items=["black", "white"],
                # Alternatives:
                # items=F["data"]["colors"],  # noqa: E800
                # items=lambda d: d["data"]["colors"],  # noqa: E800
                when=when_checked,
            ),
        ),
        id="lg",
        item_id_getter=str,
        items=["apple", "orange", "pear"],
        # Alternatives:
        # items=F["fruits"],  # noqa: E800
        # items=lambda d: d["fruits"],  # noqa: E800
    ),
    state=MessageThreadStates.message_thread_menu,
    getter=data_getter,
)


async def paging_getter(dialog_manager: DialogManager, **_kwargs):
    current_page = await dialog_manager.find(ID_STUB_SCROLL).get_page()
    return {
        "pages": 7,
        "current_page": current_page + 1,
        "day": calendar.day_name[current_page],
    }


stub_scroll_window = Window(
    Format("Вы на {current_page} странице из {pages}"),
    StaticMedia(path=Format(
        "C:/Users/darti/PycharmProjects/realogika-distributor/telegram_bot/routers/global_utils/message_thread/media/{current_page}.png")),
    StubScroll(id=ID_STUB_SCROLL, pages="pages"),
    NumberedPager(scroll=ID_STUB_SCROLL),
    Button(
        Const('Прочитать'), id='read'
    ),
    Cancel(
        Const('Закрыть'), id='close'
    ),
    state=MessageThreadStates.message_thread_menu_2,
    getter=paging_getter,
    preview_data=paging_getter,
)

message_thread_dialog = Dialog(
    message_thread_main_menu_window,
    stub_scroll_window
)
