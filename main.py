import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Log de erros
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Banco de dados simples (reseta se o bot desligar)
users_db = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in users_db:
        users_db[user.id] = 0.0
    
    texto = (
        f"👋 Olá, {user.first_name}!\n\n"
        f"💰 Seu saldo: *R$ {users_db[user.id]:.2f}*\n\n"
        "Escolha uma opção abaixo:"
    )
    
    keyboard = [
        [InlineKeyboardButton("➕ Recarregar R$ 10", callback_data="add_10")],
        [InlineKeyboardButton("🛒 Comprar Produto (R$ 5)", callback_data="comprar")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(texto, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if user_id not in users_db:
        users_db[user_id] = 0.0

    if query.data == "add_10":
        users_db[user_id] += 10.0
        await query.edit_message_text(f"✅ Saldo adicionado!\nNovo saldo: R$ {users_db[user_id]:.2f}")

    elif query.data == "comprar":
        if users_db[user_id] >= 5.0:
            users_db[user_id] -= 5.0
            await query.edit_message_text(f"🛍️ Compra realizada!\nSaldo atual: R$ {users_db[user_id]:.2f}")
        else:
            await query.edit_message_text("❌ Você não tem saldo suficiente!")

if __name__ == '__main__':
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot online!")
    app.run_polling()
