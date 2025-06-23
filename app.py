from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '8146423463:AAGsCnYb1wfksw8VpRLkI1eJ_l9Zp0P545E'
SUPPORT_USERNAME = '@supvipoficial'

# Links de pagamento por produto e por moeda
PAYMENT_LINKS = {
    'dollar': {
        'product1': 'https://buy.stripe.com/28obLG6AXgnV75K3cc',
        'product2': 'https://buy.stripe.com/6oE5ni1gD4Fdcq48wA',
        'product3': 'https://buy.stripe.com/fZe4je3oL3B92PueVa',
    },
    'euro': {
        'product1': 'https://buy.stripe.com/4gw2b6e3pb3BfCg3cd',
        'product2': 'https://buy.stripe.com/9AQ8zuf7t4FdgGkaEJ',
        'product3': 'https://buy.stripe.com/8wM4je5wT4Fd0HmfZ7',
    },
    'pound': {
        'product1': 'https://buy.stripe.com/4gM7sLgUYaTV5h61gK1RC1m',
        'product2': 'https://buy.stripe.com/cN23fa9N94Fd89O6oB',
        'product3': 'https://buy.stripe.com/bIY3fae3p5Jheyc00J',
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
