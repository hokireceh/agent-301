# Agent301 - Auto Task Claim Script

Script ini dirancang untuk mengklaim tugas secara otomatis menggunakan API. Skrip ini diimplementasikan dalam Python dan memerlukan beberapa dependensi eksternal. Petunjuk berikut akan membantu Anda menginstal dan menjalankan skrip ini di Termux.

## Prerequisites

- **Termux**: Aplikasi terminal emulator dan lingkungan Linux untuk Android.
- **Python**: Versi Python 3.x harus diinstal di Termux.

## Instalasi

Ikuti langkah-langkah berikut untuk menginstal dan menjalankan skrip di Termux:

1. **Install Termux:**
   - Unduh dan instal Termux dari [F-Droid](https://f-droid.org/packages/com.termux/).

2. **Update dan Upgrade Termux:**
```
pkg update
pkg upgrade
```

3. **Instal Python:**
```
pkg install python
```

4. **Clone Repository atau Salin Skrip:**
```
git clone https://github.com/hokireceh/agent-301.git
cd agent-301
```

5. **Edit skrip Python untuk menambahkan token bot Telegram dan chat ID Anda.**
- TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
- CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'

7. **Jalankan Skrip:**
```
python main.py
```

## Petunjuk Penggunaan
- Skrip ini akan membaca file query.txt untuk mengambil token otorisasi.
- Skrip akan secara otomatis mengklaim tugas dan mengirim pembaruan melalui Telegram.

## Troubleshooting
- Pastikan Anda memiliki koneksi internet yang stabil.
- Periksa apakah token bot Telegram dan chat ID telah dikonfigurasi dengan benar.
- Periksa file query.txt untuk memastikan format yang benar.
