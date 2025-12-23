import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("8446770330:AAHbDgoD_eF7b2KGKRSe5S5ISHuyPRpkDmA")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Link gönder (ses / video / fotoğraf)")

async def mesaj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Link alındı")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj))
    app.run_polling()

if __name__ == "__main__":
    main()
