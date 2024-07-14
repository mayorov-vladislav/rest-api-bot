from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command, or_f
from filters.chat_types import ChatTypeFilter
from sqlalchemy.ext.asyncio import AsyncSession
from common.subscribe_channels import CHANNEL_ID
from common.commands import cmd_list, adm_cmd_list
from keyboards.reply import *
from filters.chat_types import *


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


async def check_subscription(user_id: int, bot: Bot) -> list:
    not_subscribed_channels = []

    for channel in CHANNEL_ID:
        chat_id = channel
        member = await bot.get_chat_member(chat_id, user_id)
        if member.status not in ["member", "administrator", "creator"]:
            not_subscribed_channels.append(channel)

    return not_subscribed_channels


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    bot = message.bot
    not_subscribed_channels = await check_subscription(user_id, bot)

    if not_subscribed_channels:
        channels = "\n".join([f"• {channel}" for channel in not_subscribed_channels])
        await message.answer(
            f"Вы не подписаны на следующие каналы:\n{channels}\n\nПодпишитесь и повторите свой запрос."
        )
    else:
        is_admin = await is_user_admin(user_id, bot)
        if is_admin:
            for adm_cmd in adm_cmd_list:
                await message.reply(
                    f"{adm_cmd}",
                    reply_markup=admin_user_keyboard,
                )
        else:
            for user_cmd in cmd_list:
                await message.reply(
                    f"{user_cmd}",
                    reply_markup=default_user_keyboard,
                )


@user_private_router.message(Command("commands"))
@user_private_router.message(F.text == "💬Доступные команды")
async def start_cmd(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    is_admin = await is_user_admin(user_id, bot)
    if is_admin:
        for adm_cmd in adm_cmd_list:
            await message.reply(f"{adm_cmd}")
    else:
        for user_cmd in cmd_list:
            await message.reply(f"{user_cmd}")


@user_private_router.message(Command("help"))
@user_private_router.message(F.text == "💡Полезная информация")
async def ahelp(message: types.Message, bot: Bot):
    await message.reply(
        f"Ниже будет вся полезная информация для пользователей.\n\n"
        "Что бы узнать все доступные Вам команды, используйте - /commands"
    )
