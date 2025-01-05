import requests
import asyncio
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# SELECT THE CHAIN => SELECT THE WALLET THEY WANT TO TRACK => SELECT THE TIME INTERVAL THEY WANT TO BE NOTIFIED

CHAIN, WALLET, INTERVAL = range(3)

user_data = {}

# Create the function to get the information from insight api
def fetch_transactions(
        chain_id,
        client_id,
        wallet_address,
        limit=1,
        sort_by="block_number",
        sort_order="desc",
):
    try: 
        transactions_url = (f"https://{chain_id}.insight.thirdweb.com/v1/transactions")
        params = {
            "limit": limit,
            "clientId": client_id,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "filter_from_address": wallet_address,
        }

        response = requests.get(transactions_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:

        return {"error": str(e)}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Welcome to the WHALERTS Whale Tracker Bot! 🚀\n\n"
        "With this bot, you can:\n"
        "- Monitor blockchain activity. \n"
        "- Track specific wallet addresses. \n\n"
        "Use /setup to configure your bot preferences.\n"
    )
    await update.message.reply_text(welcome_text)

async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Which blockchain network do you want to work with? (e.g., Ethereum, Solana, etc.)",
        reply_markup=ReplyKeyboardMarkup(
            [["Ethereum", "Solana", "Sepolia"]], one_time_keyboard=True
        ),
    )
    return CHAIN

async def set_chain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = update.message.text
    user_data[update.effective_user.id] = {"chain": chain}
    await update.message.reply_text(
        "Please enter the wallet address you want to track!",
        reply_markup=ReplyKeyboardRemove(),
    )
    return WALLET

async def set_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallet = update.message.text
    user_data[update.effective_user.id]["wallet"] = wallet

    await update.message.reply_text(
        "How often do you want to receive updates?\n\n" "Choose in interval",
        reply_markup=ReplyKeyboardMarkup(
            [["1 minute", "1 hour", "4 hour", "12 hours"]],
            one_time_keyboard=True,
        ),
    )
    return INTERVAL


async def set_interval(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    interval_text = update.message.text
    user_id = update.effective_user.id

    interval_mapping = {
        "1 Minute": 60,
        "1 hour": 3600,
        "4 hours": 14400,
        "12 hours": 43200,
    }

    interval = interval_mapping.get(interval_text, 60)
    user_data[user_id]["interval"] = interval

    # Send confirmation to the user
    await update.message.reply_text(
        f"Setup complete🎉\n\nTracking the following:\n"
        f"- Chain: {user_data[user_id]['chain']}\n"
        f"- Wallet: {user_data[user_id]['wallet']}\n"
        f"- Update Interval: {interval_text}\n"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Setup cancelled", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def track_wallet_activity(bot, user_id):
    chain_mapping = {
        "Ethereum": 1,
        "Solana": 2212,
        "Sepolia": 11155111,
    }

    block_explorer_mapping = {
        "Ethereum": "https://etherscan.io",
        "Solana": "https://solscan.io",
        "Sepolia": "https://sepolia.etherscan.io",
    }

    while user_id in user_data:
        user_chain = user_data[user_id]["chain"]
        wallet_address = user_data[user_id]["wallet"]
        chain_id = chain_mapping.get(user_chain, 1)
        block_explorer = block_explorer_mapping.get(
            user_chain, "https://etherscan.io/tx"
        )

        transaction = fetch_transactions(chain_id, client_id, wallet_address)

        # Send the response to the user
        if "error" in transactions:
            await bot.send_message(
                user_id, f"Error fetching transactions: {transactions['error']}"
            )


def main():
    bot_token = "7618502843:AAGFj67PXpCmE18PpCvF86CnyRsa4u9JYOQ"
    application = Application.builder().token(bot_token).build()
    print("Application bot started!")

    setup_handler = ConversationHandler(
        entry_points=[CommandHandler("setup", setup)],
        states={
            CHAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_chain)],
            WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_wallet)],
            INTERVAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_interval)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add the rest of the handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(setup_handler)
    
    application.run_polling()

if __name__ == "__main__":
    main()
