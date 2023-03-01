"""Basic example for a bot that can receive payment from user."""
from config import TOKEN, PAYMENT_PROVIDER_TOKEN
import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update, LabeledPrice
from telegram.ext import Application, CommandHandler, \
    ContextTypes, ConversationHandler, MessageHandler, filters, PreCheckoutQueryHandler

STAGE_ONE, STAGE_TWO = range(2)
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)



# after (optional) shipping, it's the pre-checkout
async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the PreQecheckoutQuery"""
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if not query.invoice_payload.startswith('Custom-Payload'):
        # answer False pre_checkout_query
        await query.answer(ok=False, error_message="Сервис оплаты недоступен в данный момент. Пожалуйста, повторите попытку позже")
    else:
        await query.answer(ok=True)

# finally, after contacting the payment provider...
async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirms the successful payment."""
    # do something after successfully receiving payment
    bought = update.message.successful_payment.invoice_payload

    await update.message.reply_text("Ваш платеж получен! Вот Ваша одноразовая ссылка-приглашение:")

    chat_id = -1001669090613
    if bought == 'Custom-Payload-3':
        #letters
        chat_id = -1001625228766
    elif bought == 'Custom-Payload-2':
        #45 min
        chat_id = -1001862709465

    invite_link = await context.bot.create_chat_invite_link(chat_id=chat_id, member_limit=1)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=invite_link.invite_link)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    #pics source is here: https://kidsskazki.ru/pictures
    await context.bot.send_invoice(chat_id=update.effective_chat.id,
                                   title="Кот Огонëк короткие сказки",
                                   description="Сказки для быстрого засыпания",
                                   provider_token=PAYMENT_PROVIDER_TOKEN,
                                   payload = "Custom-Payload-1",
                                   prices=[LabeledPrice("Кот Огонëк короткие сказки", 10000)],
                                   currency='RUB',
                                   photo_url='https://thumb.tildacdn.com/tild6631-3166-4163-a162-323036373962/-/format/webp/____1024.jpg',
                                   photo_width=416,
                                   photo_height=416,
                                   photo_size=416,
                                   protect_content=True,
                                   )
    await context.bot.send_invoice(chat_id=update.effective_chat.id,
                                   title="Кот Огонëк 45 минут",
                                   description="Длинная сказка для быстрого засыпания",
                                   provider_token=PAYMENT_PROVIDER_TOKEN,
                                   payload = "Custom-Payload-2",
                                   prices=[LabeledPrice("Кот Огонëк короткие сказки", 15000)],
                                   currency='RUB',
                                   photo_url='https://thumb.tildacdn.com/tild6139-3164-4664-a135-323136313164/-/format/webp/1675765768559.jpg',
                                   photo_width=416,
                                   photo_height=416,
                                   photo_size=416,
                                   protect_content=True,
                                   )
    await context.bot.send_invoice(chat_id=update.effective_chat.id,
                                   title="Буквы",
                                   description="28 сказок про буквы",
                                   provider_token=PAYMENT_PROVIDER_TOKEN,
                                   payload="Custom-Payload-3",
                                   prices=[LabeledPrice("28 сказок про буквы", 20000)],
                                   currency='RUB',
                                   photo_url='https://thumb.tildacdn.com/tild3239-3537-4262-a366-373739623239/-/format/webp/___2400_5.jpg',
                                   photo_width=416,
                                   photo_height=416,
                                   photo_size=416,
                                   protect_content=True,
                                   )
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Повторить список сказок для покупки: /start .")


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="До свидания!")

    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Начните диалог с ботом командой /start .")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()


    application.add_handler(CommandHandler("start", start))
    # Pre-checkout handler to final check
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    # Success! Notify your user!
    application.add_handler(
        MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback)
    )

    #help handler
    application.add_handler(CommandHandler("help", help_command))
    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()