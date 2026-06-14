import sys
import types

# =========================================================
# CRITICAL FIX FOR PYTHON 3.14 COMPATIBILITY WITH TELEGRAM
# =========================================================
from telegram.ext import Updater
if not hasattr(Updater, '_Updater__polling_cleanup_cb'):
    # Inject the missing internal attribute to bypass Python 3.14 type slot restriction
    setattr(Updater, '_Updater__polling_cleanup_cb', None)
# =========================================================

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

FIREBASE_URL = "https://hry-study-default-rtdb.firebaseio.com/inbox.json"
TOKEN = '8858220246:AAE5LE6j6Nr7LC4iRt7_mLBou_ifuB1-5bY'

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video
    caption = update.message.caption or "No Caption"
    file_id = video.file_id

    data = {
        "video_id": file_id,
        "caption": caption
    }
    
    try:
        response = requests.post(FIREBASE_URL, json=data)
        if response.status_code == 200:
            await update.message.reply_text("✅ Video successfuly synced to Admin Inbox!")
        else:
            await update.message.reply_text("❌ Firebase Error!")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    print("Bot is running perfectly...")
    application.run_polling()
