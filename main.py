from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if user_id not in users:
        users[user_id] = 0
    
    menu = [["💰 Saldo", "➕ Recarregar"], ["🛒 Comprar"]]
    markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)

    await update.message.reply_text("Bem-vindo ao bot!", reply_markup=markup)

async def mensagens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    texto = update.message.text

    if texto == "💰 Saldo":
        saldo = users.get(user_id, 0)
        await update.message.reply_text(f"Seu saldo é: R${saldo}")

    elif texto == "➕ Recarregar":
        await update.message.reply_text("Envie R$10 via Pix: SUA_CHAVE_AQUI")

    elif texto == "🛒 Comprar":
        saldo = users.get(user_id, 0)
        if saldo >= 10:
            users[user_id] -= 10
            await update.message.reply_text("Compra realizada!")
        else:
            await update.message.reply_text("Saldo insuficiente.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, mensagens))

app.run_polling()
