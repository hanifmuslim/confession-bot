import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get config from environment
BOT_TOKEN = os.environ['8006129358:AAElFwaLQMPYOeS4l97Cti8uNISU0Kw0RZs']
ADMIN_CHAT_ID = os.environ['663072655']
TARGET_CHAT_ID = os.environ['-1002096830555']

pending_confessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤫 Send your confession!")

async def handle_confession(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        await update.message.reply_text("❌ Please message me privately!")
        return
    
    user_id = update.message.from_user.id
    confession_text = update.message.text
    pending_confessions[user_id] = confession_text
    
    keyboard = [[InlineKeyboardButton("✅ Confirm", callback_data="confirm")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Confirm to send anonymously:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    
    if query.data == "confirm" and user_id in pending_confessions:
        confession_text = pending_confessions[user_id]
        confession_message = f":\n\n{confession_text}"
        
        await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=confession_message)
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"New confession: {confession_text}")
        await query.edit_message_text("✅ Confession sent!")
        del pending_confessions[user_id]

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_confession))
    
    print("🤖 Bot running...")
    application.run_polling()

if __name__ == '__main__':
    main()
