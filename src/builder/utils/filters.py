from collections.abc import Callable
from typing import Any

import regex as re
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message

from src import BOT_ADMINS
from src.builder.db.crud import get_whitelist
from src.common.utils.i18n import get_user_language


def check_if_token_reply(_: Callable[..., Any], __: Client, message: Message) -> bool:
    if not message.reply_to_message or not message.text:
        return False
    
    # Check if the reply is to the token request message
    reply_text = message.reply_to_message.text or ""
    expected_text = get_user_language(message)('reply_with_token')
    
    # Only check if the reply text matches the expected token request text
    if reply_text != expected_text:
        return False
    
    # Check if the message text matches bot token format
    token_match = re.search(r'^\d{8,20}:[A-Za-z0-9_-]{35}$', message.text.strip())
    
    if token_match:
        print(f"[DEBUG] Valid token reply detected: {message.text}")
    
    return bool(token_match)


def check_if_custom_message_reply(_: Callable[..., Any], __: Client, message: Message) -> bool:
    return bool(
        message.reply_to_message.reply_markup
        and message.reply_to_message.reply_markup.inline_keyboard
        and any(
            re.search(r'^mb[mrcs]_\d+$', button.callback_data)
            for row in message.reply_to_message.reply_markup.inline_keyboard
            for button in row
        )
    )


is_token_reply = filters.create(check_if_token_reply)
is_custom_message_reply = filters.create(check_if_custom_message_reply)


def is_whitelisted_user() -> filters.Filter:
    def check_if_whitelisted(
        _: Callable[[Any], bool], __: Client, update: Message | CallbackQuery
    ) -> bool:
        whitelist = get_whitelist()
        if not whitelist:
            return True  # Allow all if whitelist is empty
        return bool(
            update.from_user
            and (update.from_user.id in whitelist or update.from_user.id in BOT_ADMINS)
        )

    return filters.create(check_if_whitelisted)
