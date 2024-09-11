import requests
import urllib.parse
from fake_useragent import UserAgent
import time
import json
from telegram import Bot

# Telegram bot setup
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'
bot = Bot(token=TELEGRAM_TOKEN)

# Fungsi untuk mengirim pesan ke Telegram
def send_telegram_message(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

# Fungsi untuk memecah data dan mengambil username dari authorization token atau user data
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

# Fungsi untuk membaca authorization dari file query.txt
def load_authorizations_with_usernames(file_path):
    with open(file_path, 'r') as file:
        authorizations = file.readlines()

    auth_with_usernames = [{'authorization': auth.strip(), 'username': extract_username(auth)} for auth in authorizations]
    return auth_with_usernames

# Fungsi untuk klaim task
def claim_tasks(authorization, account_number, username):
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
            send_telegram_message(message)

            tasks = result.get("tasks", [])
            for task in tasks:
                task_type = task.get("type")
                title = task.get("title")
                reward = task.get("reward", 0)
                is_claimed = task.get("is_claimed")
                count = task.get("count", 0)
                max_count = task.get("max_count")

                if max_count is None and not is_claimed:
                    claim_task(headers, task_type, title)

                elif task_type == "video" and count < max_count:
                    while count < max_count:
                        progress_message = f"#TASK {task_type} - {title} PROGRESS: {count}/{max_count}"
                        send_telegram_message(progress_message)
                        if claim_task(headers, task_type, title):
                            count += 1
                        else:
                            break

                elif not is_claimed and count >= max_count:
                    claim_task(headers, task_type, title)
            send_telegram_message("SEMUA TASK DONE!")
        else:
            send_telegram_message("GAGAL MENGAMBIL TASK. ULANGI BREKK.")
    else:
        send_telegram_message(f"# HTTP Error: {response.status_code}")

def claim_task(headers, task_type, title):
    url_complete_task = 'https://api.agent301.org/completeTask'
    claim_data = {"type": task_type}
    response = requests.post(url_complete_task, headers=headers, json=claim_data)

    if response.status_code == 200 and response.json().get("ok"):
        result = response.json().get("result", {})
        task_reward = result.get("reward", 0)
        balance = result.get("balance", 0)
        message = f"#TASK {task_type} - {title} - REWARD {task_reward} AP - BALANCE NOW: {balance} AP"
        send_telegram_message(message)
        return True
    else:
        message = f"#TASK {task_type} - {title} - GAGAL CLAIM!"
        send_telegram_message(message)
        return False

# Fungsi utama untuk menjalankan seluruh proses
def main():
    auth_data = load_authorizations_with_usernames('query.txt')

    while True:
        for account_number, data in enumerate(auth_data, start=1):
            authorization = data['authorization']
            username = data['username']

            # Menampilkan informasi tentang akun yang sedang dijalankan
            message = f"\n------------------------------------\n  ## ACCOUNT #{account_number} ##\n------------------------------------"
            send_telegram_message(message)

            claim_tasks(authorization, account_number, username)

        send_telegram_message("AUTO LOOPING SETELAH 8 JAM...")
        time.sleep(28800)  # 8 jam dalam detik
        
if __name__ == "__main__":
    main()
