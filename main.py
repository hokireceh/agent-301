import requests
import urllib.parse
from fake_useragent import UserAgent
import time
import json
from telegram import Bot
from dotenv import load_dotenv
import os
import asyncio

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Konfigurasi bot Telegram dari variabel lingkungan
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

def extract_username(authorization):
    try:
        # Memecah string query
        parsed_data = urllib.parse.parse_qs(authorization)
        user_data_json = parsed_data.get('user', [''])[0]

        # Decode URL encoded string menjadi JSON
        user_data = json.loads(urllib.parse.unquote(user_data_json))

        # Mengambil username dari JSON
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
            await send_telegram_message(message)
            print(message)

            tasks = result.get("tasks", [])
            for task in tasks:
                task_type = task.get("type")
                title = task.get("title")
                reward = task.get("reward", 0)
                is_claimed = task.get("is_claimed")
                count = task.get("count", 0)
                max_count = task.get("max_count")

                if max_count is None and not is_claimed:
                    await claim_task(headers, task_type, title, username)

                elif task_type == "video" and count < max_count:
                    while count < max_count:
                        print(f"#TASK {task_type} - {title} PROGRESS: {count}/{max_count}")
                        if await claim_task(headers, task_type, title, username):
                            count += 1
                        else:
                            break

                elif not is_claimed and count >= max_count:
                    await claim_task(headers, task_type, title, username)
            await send_telegram_message("SEMUA TASK DONE!")
        else:
            await send_telegram_message("GAGAL MENGAMBIL TASK. ULANGI BREKK.")
    else:
        await send_telegram_message(f"# HTTP Error: {response.status_code}")

    return balance  # Pastikan balance dikembalikan setelah semua tugas diproses

async def claim_task(headers, task_type, title, username):
    url_complete_task = 'https://api.agent301.org/completeTask'
    claim_data = {"type": task_type}
    response = requests.post(url_complete_task, headers=headers, json=claim_data)

    if response.status_code == 200 and response.json().get("ok"):
        result = response.json().get("result", {})
        task_reward = result.get("reward", 0)
        balance = result.get("balance", 0)
        message = f"#TASK {task_type} - {title} - REWARD {task_reward} AP - BALANCE NOW: {balance} AP"
        await send_telegram_message(message)
        print(message)
        return True
    else:
        message = f"#TASK {task_type} - {title} - GAGAL CLAIM!"
        await send_telegram_message(message)
        print(message)
        return False

async def main():
    auth_data = load_authorizations_with_usernames('query.txt')

    while True:
        total_balance = 0  # Initialize total balance
        for account_number, data in enumerate(auth_data, start=1):
            authorization = data['authorization']
            username = data['username']
            
            # Menampilkan informasi tentang akun yang sedang dijalankan
            message = f"\n------------------------------------\n  ## ACCOUNT #{account_number} ##\n------------------------------------"
            await send_telegram_message(message)
            print(message)

            balance = await claim_tasks(authorization, account_number, username)
            if balance:
                total_balance += balance  # Accumulate total balance

        # Kirimkan total saldo setelah semua akun diproses
        total_message = f"TOTAL SALDO DARI SEMUA AKUN: {total_balance} AP"
        await send_telegram_message(total_message)
        print(total_message)

        await send_telegram_message("AUTO LOOPING SETELAH 8 JAM...")
        print("AUTO LOOPING SETELAH 8 JAM...")
        await asyncio.sleep(28800)  # 8 jam dalam detik

if __name__ == "__main__":
    asyncio.run(main())
