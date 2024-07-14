from string import punctuation
from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command, or_f
from filters.chat_types import ChatTypeFilter
from sqlalchemy.ext.asyncio import AsyncSession
from common.resticted_words import restricted_words


user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))


@user_group_router.message(Command("updateadminlist"))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    chat_admin_list = await bot.get_chat_administrators(chat_id)

    admin_list = [
        member.user.id
        for member in chat_admin_list
        if member.status == "creator" or member.status == "administrator"
    ]

    with open("admin_id_list.txt", "w") as file:
        for member in chat_admin_list:
            if member.status == "creator" or member.status == "administrator":
                if member.user.username:
                    file.write(f"{member.user.username} - {member.user.id}\n")
                else:
                    file.write(f"{member.user.full_name} - {member.user.id}\n")

    bot.my_admin_list = admin_list

    if message.from_user.id in admin_list:
        await message.delete()
        print(
            f"Сообщение от @{message.from_user.username}, id - [{message.from_user.id}] удалено"
        )
    else:
        await message.delete()
        await message.answer(
            f"@{message.from_user.username}, данная команда вам недоступна! \nНе стоит использовать ее просто так."
        )
        print(
            f"Сообщение от @0{message.from_user.username}, id - [{message.from_user.id}] удалено, так как у отправителя недостаточно прав для использования данной команды"
        )


def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))


@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(
            f"{message.from_user.first_name}, соблюдайте порядок общения в чате!"
        )
        await message.delete()
