import uuid


async def uuid_generation():
    return str(uuid.uuid1())


async def split_name_id_promocode(input_string):
    promocode_id, _, promocode_name = input_string.partition('_')
    return promocode_id, promocode_name
