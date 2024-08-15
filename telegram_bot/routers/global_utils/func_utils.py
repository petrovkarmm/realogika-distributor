import uuid
import qrcode

from aiofiles import os
from aiogram.types import FSInputFile, Message
from settings import BOT_BASE_DIR


async def uuid_generation():
    return str(uuid.uuid1())


async def split_name_id_promocode(input_string):
    promocode_id, _, promocode_name = input_string.partition('_')
    return promocode_id, promocode_name


async def send_ref_link_with_qr(ref_link: str,
                                message: Message):
    img = qrcode.make(ref_link)

    file_uuid_name = uuid.uuid4()

    qr_path = f"{BOT_BASE_DIR}\\routers\\global_utils\\qr_codes\\{file_uuid_name}.png"

    img.save(qr_path)

    photo = FSInputFile(qr_path)

    await message.answer(
        text='Ваша реферальная ссылка: \n'
             f'{ref_link}'
    )

    try:
        await message.answer_photo(
            photo=photo
        )
    except Exception as e:
        print(e)

    try:
        await os.remove(qr_path)
    except Exception as e:
        print(e)
