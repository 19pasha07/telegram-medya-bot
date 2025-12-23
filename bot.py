import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")

user_links = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Link gönder (ses / video / fotoğraf)")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text
    user_links[update.message.chat_id] = link

    keyboard = [
        [InlineKeyboardButton("🎵 Ses (MP3)", callback_data="audio")],
        [InlineKeyboardButton("🎬 Video (MP4)", callback_data="video")],
        [InlineKeyboardButton("🖼 Fotoğraf", callback_data="photo")]
    ]

    await update.message.reply_text(
        "Ne indirmek istiyorsun?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    link = user_links.get(query.message.chat_id)
    choice = query.data

    ydl_opts = {}

    if choice == "audio":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'media.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3'
            }]
        }
    elif choice == "video":
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': 'media.%(ext)s'
        }
    elif choice == "photo":
        ydl_opts = {
            'skip_download': True
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=(choice != "photo"))

    if choice == "photo":
        photo_url = info['thumbnails'][-1]['url']
        await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo_url)
        return

    file_name = next(f for f in os.listdir('.') if f.startswith('media.'))

    if choice == "audio":
        await context.bot.send_audio(chat_id=query.message.chat_id, audio=open(file_name, 'rb'))
    elif choice == "video":
        await context.bot.send_video(chat_id=query.message.chat_id, video=open(file_name, 'rb'))

    os.remove(file_name)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.add_handler(CallbackQueryHandler(download))
app.run_polling()
