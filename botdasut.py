import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandObject

# O'zingizning tokeningizni yozing
API_TOKEN = "8578503116:AAEvZFhUqychs1mXOowxKB8heQT6-EPZeEY"

# Bot egasining (Sizning) Telegram ID raqamingiz (buni @userinfobot orqali bilish mumkin)
 ADMIN_ID = 123456789  # <--- O'zingizning ID raqamingizni yozing (sonlarda)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Fayllar ID'sini saqlash uchun virtual baza
fayllar_bazasi = {}

@dp.message()
async def qidiruv_tizimi(message: types.Message):
    global fayllar_bazasi
    
    # 1. Agar ADMIN botga fayl (PDF/hujjat) tashlasa, bot uning IDsini eslab qoladi
    if message.document and message.from_user.id == ADMIN_ID:
        file_id = message.document.file_id
        file_name = message.document.file_name.lower()
        fayllar_bazasi[file_name] = file_id
        await message.answer(f"✅ Fayl bazaga qo'shildi: {message.document.file_name}")
        return

    text = message.text
    if not text:
        return

    if text.startswith('/search'):
        query = text.replace('/search', '').strip().lower()
    else:
        query = text.strip().lower()
    
    if not query or text == "/start":
        await message.answer("📚 Botga xush kelibsiz! Fayl nomini yozing yoki `/search fayl_nomi` deb qidiring.")
        return

    # 2. Qidiruv qismi
    topilgan_fayllar = []
    for f_name, f_id in fayllar_bazasi.items():
        if query in f_name:
            topilgan_fayllar.append((f_name, f_id))

    if topilgan_fayllar:
        await message.answer(f"🔍 {len(topilgan_fayllar)} ta fayl topildi. Yuborilmoqda...")
        for name, file_id in topilgan_fayllar:
            await message.bot.send_document(chat_id=message.chat.id, document=file_id)
    else:
        await message.answer("😔 Afsuski, bunday fayl topilmadi.")

async def main():
    # Xosting porti uchun majburiy sozlama
    import threading
    from http.server import HTTPServer, BaseHTTPRequestHandler
    class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running!")
    
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

    print("🤖 Bot hostda ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
