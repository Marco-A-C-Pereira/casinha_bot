import asyncio
import telegram
import modules.telegram_bot.tokens as tokens
import modules.database as db
from datetime import datetime

def time_converter(ISO8601):
    date_object = datetime.strptime(ISO8601, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_object.strftime("%d/%m/%Y")

def description_fixer(text):
    newtext = text
    for target in ["<br>", "<b>", "</b>", "<i>", "</i>"]:
        if target in text: newtext = newtext.replace(target, " ")

    newtext = newtext.lower()
    return newtext.title()

def message_builder(listing):
    character_number = 250 
    

    message = f"""
❗️ {listing["title"]}
🏠 Endereço: {listing["neighborhood"]}-{listing["street"]}-{listing["number"]}
💰 Preço mensal: R${listing["total_monthly_price"]}R$
🛌 Quartos: {listing["bedrooms"]}
🔎 {description_fixer(listing["description"])[:character_number]}

🔗 [Acesse aqui o imóvel, bicha]({listing["link"]})
⚡️ Telefone: {listing['whats']}
🕑 Atualizado / Criado:
{time_converter(listing["update_date"])} | {time_converter(listing["creation_date"])}
"""
    return message

def media_converter(url_list):
    media_photo_list = []

    for item in url_list:
        media_photo_list.append(telegram.InputMediaPhoto(media=item))

    return media_photo_list

async def core():
    smallList = db.request_local_list()
    bot = telegram.Bot(tokens.telegram_bot_token)
    async with bot:
        for listing in smallList[:2]:
            media_list = media_converter(listing["images_url"])

            await bot.send_media_group(caption=message_builder(listing), media=media_list ,parse_mode="markdown", chat_id=tokens.valid_users[0])
            # await bot.sendMessage(text=message_builder(listing), parse_mode="markdown", chat_id=tokens.valid_users[0])

# async def core():
#     bot = telegram.Bot(tokens.telegram_bot_token)
#     async with bot:
#         # updates = (await bot.get_updates())[0].message.from_user.id
#         updates = (await bot.get_updates())
#         print(updates)
#         # print(await bot.get_me())

def main():
    # print(smallList[0]['link'])
    asyncio.run(core())
