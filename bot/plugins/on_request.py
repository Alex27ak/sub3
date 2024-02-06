from pyrogram import Client
from pyrogram.types import ChatJoinRequest


@Client.on_chat_join_request()
async def on_chat_join_request(client, chat_join_request: ChatJoinRequest):
    name = chat_join_request.invite_link.name
    if int(name) == chat_join_request.from_user.id:
        await chat_join_request.approve()
