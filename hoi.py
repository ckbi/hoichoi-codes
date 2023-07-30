import random
import re
import asyncio
import requests
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

API_TOKEN = '6309006558:AAFWWhDcqlk9S0BztYDB5afhWk1PdMI-7GA'  # Replace with your API token
USERNAME = '' # Replace with your username

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

def coupon_check(redeem_code): 
    options_url = "https://prod-api.viewlift.com/subscription/offer/validate?site=hoichoitv" 
    post_url = "https://prod-api.viewlift.com/subscription/offer/validate?site=hoichoitv" 
 
    headers = { 
        "Accept": "*/*", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8", 
        "Access-Control-Request-Headers": "authorization,content-type,x-api-key", 
        "Access-Control-Request-Method": "POST", 
        "Origin": "https://www.hoichoi.tv", 
        "Referer": "https://www.hoichoi.tv/", 
        "Sec-Fetch-Dest": "empty", 
        "Sec-Fetch-Mode": "cors", 
        "Sec-Fetch-Site": "cross-site", 
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36" 
    } 
 
    post_headers = { 
        "Accept": "application/json, text/plain, */*", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8", 
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiJlYmE2YzM0My01NGM5LTQzYTQtODcyNy1kYTM3MGVlNjhmNWMiLCJzaXRlIjoiaG9pY2hvaXR2Iiwic2l0ZUlkIjoiN2ZhMGVhOWEtOTc5OS00NDE3LTk5ZjUtY2JiNTM0M2M1NTFkIiwiZW1haWwiOiJibGFja3doaXRlbWFzdW0uMUBnbWFpbC5jb20iLCJpcGFkZHJlc3NlcyI6IjY1LjIwLjgwLjQ2LCAxMC4xMjAuMTUuMTU0LCA1Mi41NS4yMDguMjQzLCAxMzAuMTc2Ljk4Ljc5IiwiY291bnRyeUNvZGUiOiJJTiIsInBvc3RhbGNvZGUiOiI0MDAwNzIiLCJwcm92aWRlciI6Imdvb2dsZSIsImRldmljZUlkIjoiYnJvd3Nlci03ZjYwZTEyOC1hYTQwLWE3OGYtZDVlMC04ZTdhMDFiZjRhNTEiLCJpYXQiOjE2ODgwOTMwODcsImV4cCI6MTY4ODY5Nzg4N30.-jSTDWTcTPCwSuP4LSeVMW3xpbow2x41hf9UzVpSnSY", 
        "Content-Length": "29", 
        "Content-Type": "application/json;charset=UTF-8", 
        "Origin": "https://www.hoichoi.tv", 
        "Referer": "https://www.hoichoi.tv/", 
        "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"", 
        "Sec-Ch-Ua-Mobile": "?1", 
        "Sec-Ch-Ua-Platform": "\"Android\"", 
        "Sec-Fetch-Dest": "empty", 
        "Sec-Fetch-Mode": "cors", 
        "Sec-Fetch-Site": "cross-site", 
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", 
        "X-Api-Key": "PBSooUe91s7RNRKnXTmQG7z3gwD2aDTA6TlJp6ef" 
    } 
 
    options_response = requests.options(options_url, headers=headers) 
    allowed_methods = options_response.headers.get("Access-Control-Allow-Methods") 
    allowed_headers = options_response.headers.get("Access-Control-Allow-Headers") 
 
    payload = {"offerCode": redeem_code} 
    post_response = requests.post(post_url, headers=post_headers, json=payload) 

@dp.message_handler(commands=['hoi'])
async def hoi_handler(message: types.Message):
    redeem_codes = message.text.split()[1:]
    if not redeem_codes:
        await message.reply("Please provide at least one redeem code.")
        return

    loading_message = await bot.send_message(message.chat.id, "Checking codes... Please wait.")

    valid_codes = []
    invalid_codes = []

    for redeem_code in redeem_codes:
        if coupon_check(redeem_code):
            valid_codes.append(redeem_code)
        else:
            invalid_codes.append(redeem_code)

    await bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)

    response_text = ""

    if valid_codes:
        response_text += f"Valid codes:\n{' '.join(valid_codes)}\n\n"
    if invalid_codes:
        response_text += f"Invalid codes:\n{' '.join(invalid_codes)}\n\n"
    if not response_text:
        response_text = "No valid codes found."

    await message.reply(response_text)

@dp.message_handler(commands=['generate'])
async def generate_handler(message: types.Message):
    try:
        count = int(message.text.split()[1])
    except (ValueError, IndexError):
        await message.reply("Please provide the number of codes to generate. Example: /generate 10")
        return

    codes = []
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    for _ in range(count):
        generated_code = "HOSCN-I6" + "".join(random.choices(characters, k=4))
        codes.append(generated_code)
    
    response_text = "\n".join([f"CODE = {code} | PLAN = MONTHLY | BY = @{USERNAME}" for code in codes])
    await message.reply(response_text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
