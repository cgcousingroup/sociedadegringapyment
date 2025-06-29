from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '7608134150:AAENGiLeMCxSnmwwmNiMXro4BxUWo9fUO_4'
SUPPORT_USERNAME = '@suppvipoficial'

# Links de pagamento por produto e por moeda
PAYMENT_LINKS = {
    'dollar': {
        'product1': 'https://buy.stripe.com/dRm28jcqG6iP1A0dIO4AU00',
        'product2': 'https://buy.stripe.com/14A4gr3UaePlguU9sy4AU01',
        'product3': 'https://buy.stripe.com/14A7sD4Ye4aH92sfQW4AU02',
    },
    'euro': {
        'product1': 'https://buy.stripe.com/aFa4gr2Q6dLh4McawC4AU03',
        'product2': 'https://buy.stripe.com/4gMeV5fCScHd1A02064AU04',
        'product3': 'https://buy.stripe.com/8x2dR176m6iPceE7kq4AU05',
    },
    'pound': {
        'product1': 'https://buy.stripe.com/cNi14f2Q68qX92s7kq4AU06',
        'product2': 'https://buy.stripe.com/6oUeV562i6iPguU34a4AU07',
        'product3': 'https://buy.stripe.com/28E3cngGWbD9a6w9sy4AU08',
    }
}

# Dicionário pra guardar a escolha de moeda por usuário
user_currency = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("💵 Dollar", callback_data='currency_dollar'),
            InlineKeyboardButton("💶 Euro", callback_data='currency_euro'),
            InlineKeyboardButton("💷 Pound", callback_data='currency_pound'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌍 Choose your currency:", reply_markup=reply_markup)

async def currency_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    currency = query.data.replace('currency_', '')
    user_currency[query.from_user.id] = currency

    keyboard = [
        [
            InlineKeyboardButton("🔥 Prohibition", callback_data='product_product1'),
            InlineKeyboardButton("🔥 Amateur", callback_data='product_product2'),
            InlineKeyboardButton("🔥 Girl HighSchool", callback_data='product_product3'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"You selected *{currency.upper()}*.\n\nNow choose your product:", parse_mode="Markdown", reply_markup=reply_markup)

async def product_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    product = query.data.replace('product_', '')
    currency = user_currency.get(query.from_user.id)

    if currency and product:
        payment_link = PAYMENT_LINKS.get(currency, {}).get(product)
        if payment_link:
            message = (
                f"✅ You selected *{product.upper()}* with *{currency.upper()}*.\n\n"
                f"👉 Please pay using the link below:\n\n"
                f"{payment_link}\n\n"
                f"Or Pay using Paypal: ```laurajordana90@gmail.com```\n\n"
                f"📩 After payment, send your receipt to: {SUPPORT_USERNAME}"
            )
            await query.edit_message_text(message, parse_mode="Markdown")
        else:
            await query.edit_message_text("❌ Payment link not found. Please try again.")
    else:
        await query.edit_message_text("❌ Session expired. Please type /start again.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(currency_selected, pattern='^currency_'))
    app.add_handler(CallbackQueryHandler(product_selected, pattern='^product_'))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
