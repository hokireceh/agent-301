# Agent301 - Auto Task Claim Script

Script ini dirancang untuk mengklaim tugas secara otomatis menggunakan API. Skrip ini diimplementasikan dalam Python dan memerlukan beberapa dependensi eksternal. Petunjuk berikut akan membantu Anda menginstal dan menjalankan skrip ini di Termux.

## 📢 Telegram Group

Join our Telegram group to stay updated and get instructions on how to use this tool:

- [Garapan Airdrop - Channel](https://t.me/garapanairdrop_indonesia)
- [Sobat Ongkang Ongkang - Group](https://t.me/ongkang_ongkang)
- [I recommend you use VPS](https://console.idcloudhost.com/referral/1n60rk)
- If you want to buy a VPS at Kaimi, please DM us

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

5. **Edit skrip .env untuk menambahkan token bot Telegram dan chat ID Anda.**
- TELEGRAM_TOKEN=
- CHAT_ID=

6. **Instal Dependensi:**
```
pip install -r requirements.txt
```

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
