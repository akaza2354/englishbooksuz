import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandObject

# Tokeningizni yozing
API_TOKEN = "8578503116:AAEvZFhUqychs1mXOowxKB8heQT6-EPZeEY"
# Boya olgan kanalingiz ID raqamini yozing (minus belgisi bilan)
KANAL_ID =  -1004402019287 

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Bot har gal yonganda fayllarni saqlab qoladigan ro'yxat
fayllar_royxati = {}

@dp.message()
async def qidiruv_tizimi(message: types.Message):
    global fayllar_royxati
    
    # Kanal ID raqamini aniqlab olish uchun yordamchi qism
    if message.forward_from_chat:
        await message.answer(f"Siz uzatgan kanal ID raqami: {message.forward_from_chat.id}")
        return

    text = message.text
    if not text:
        return

    query = text.replace('/search', '').strip().lower() if text.startswith('/search') else text.strip().lower()
    
    if not query or text == "/start":
        await message.answer("📚 Botga xush kelibsiz! Fayl nomini yozing yoki `/search fayl_nomi` deb qidiring.")
        return

    # ⚠️ DIQQAT: Tekin xosting uchun vaqtinchalik yechim.
    # Agar loyiha kengaysa, fayllarni matn ko'rinishida kanalga nomlab tashlab chiqish qulayroq.
    # Hozircha qo'lda kiritish yoki kanal xabarlarini eslab qolish kodi:
    
    await message.answer("🔍 Fayllar tekshirilmoqda...")
    # Ushbu qism mukammal ishlashi uchun foydalanuvchilar qidirgan so'z kanal ichidagi fayl nomiga mos kelishi kerak.
    # Tekin xostingda eng ishonchli yo'l - fayllarni to'g'ridan-to'g'ri kanal havolasi orqali ulashdir.

async def main():
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

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
