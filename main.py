import requests
import urllib.parse
from fake_useragent import UserAgent
import time
import json
import os
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio

# Load environment variables from .env file
load_dotenv()

# Get the Telegram bot token and chat ID from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Initialize Telegram bot
app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

async def send_telegram_message(message):
    await app.bot.send_message(chat_id=CHAT_ID, text=message)

def extract_username(authorization):
    try:
        parsed_data = urllib.parse.parse_qs(authorization)
        user_data_json = parsed_data.get('user', [''])[0]
        user_data = json.loads(urllib.parse.unquote(user_data_json))
        username = user_data.get('username', 'unknown')
        return username
    except (json.JSONDecodeError, KeyError):
        return 'unknown'

def load_authorizations_with_usernames(file_path):
    with open(file_path, 'r') as file:
        authorizations = file.readlines()
    auth_with_usernames = [{'authorization': auth.strip(), 'username': extract_username(auth)} for auth in authorizations]
    return auth_with_usernames

async def claim_tasks(authorization, account_number, username):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'authorization': authorization.strip(),
        'origin': 'https://telegram.agent301.org',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    url_get_tasks = 'https://api.agent301.org/getMe'
    response = requests.post(url_get_tasks, headers=headers)

    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("ok"):
            result = json_response.get("result", {})
            balance = result.get("balance", 0)
            message = f"#ACCOUNT {username} | BALANCE: {balance} AP\nMENJALANKAN AUTO CLAIM TASK...\n"
            print(message)
            await send_telegram_message(message)

            tasks = result.get("tasks", [])
            for task in tasks:
                task_type = task.get("type")
                title = task.get("title")
                reward = task.get("reward", 0)
                is_claimed = task.get("is_claimed")
                count = task.get("count", 0)
                max_count = task.get("max_count")

                if max_count is None and not is_claimed:
                    await claim_task(headers, task_type, title)

                elif task_type == "video" and count < max_count:
                    while count < max_count:
                        print(f"#TASK {task_type} - {title} PROGRESS: {count}/{max_count}")
                        if await claim_task(headers, task_type, title):
                            count += 1
                        else:
                            break

                elif not is_claimed and count >= max_count:
                    await claim_task(headers, task_type, title)
            print("\nSEMUA TASK DONE!")
        else:
            error_message = "GAGAL MENGAMBIL TASK. ULANGI BREKK."
            print(error_message)
            await send_telegram_message(error_message)
    else:
        http_error_message = f"# HTTP Error: {response.status_code}"
        print(http_error_message)
        await send_telegram_message(http_error_message)

async def claim_task(headers, task_type, title):
    url_complete_task = 'https://api.agent301.org/completeTask'
    claim_data = {"type": task_type}
    response = requests.post(url_complete_task, headers=headers, json=claim_data)

    if response.status_code == 200 and response.json().get("ok"):
        result = response.json().get("result", {})
        task_reward = result.get("reward", 0)
        balance = result.get("balance", 0)
        task_message = f"#TASK {task_type} - {title} - REWARD {task_reward} AP - BALANCE NOW: {balance} AP"
        print(task_message)
        return True
    else:
        task_fail_message = f"#TASK {task_type} - {title} - GAGAL CLAIM!"
        print(task_fail_message)
        await send_telegram_message(task_fail_message)
        return False

async def main():
    auth_data = load_authorizations_with_usernames('query.txt')

    while True:
        for account_number, data in enumerate(auth_data, start=1):
            authorization = data['authorization']
            username = data['username']
            account_message = f"\n------------------------------------\n  ## ACCOUNT #{account_number} ##\n------------------------------------"
            print(account_message)
            await send_telegram_message(account_message)

            await claim_tasks(authorization, account_number, username)

        loop_message = "AUTO LOOPING SETELAH 8 JAM..."
        print(loop_message)
        await send_telegram_message(loop_message)
        await asyncio.sleep(28800)  # 8 jam dalam detik

if __name__ == "__main__":
    asyncio.run(main())
