"""Basic example for a bot that can receive payment from user."""
from config import TOKEN, PAYMENT_PROVIDER_TOKEN
import logging

from telegram import __version__ as TG_VER

from goods import get_goods

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

pricelist = get_goods()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)



# the pre-checkout
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

    chat_id = pricelist[update.message.successful_payment.invoice_payload].telegram_channel_id

    await update.message.reply_text("Ваш платеж получен! Вот Ваша одноразовая ссылка-приглашение:")



    invite_link = await context.bot.create_chat_invite_link(chat_id=chat_id, member_limit=1)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=invite_link.invite_link)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends messages with items attached."""
    #pics source is here: https://kidsskazki.ru/pictures
    for item in pricelist.values():
        await context.bot.send_invoice(chat_id=update.effective_chat.id,
                                   title=item.title,
                                   description=item.description,
                                   provider_token=PAYMENT_PROVIDER_TOKEN,
                                   payload = item.payload,
                                   prices=[LabeledPrice(item.title, item.price*100)],
                                   currency='RUB',
                                   photo_url=item.photo_url,
                                   photo_width=416,
                                   photo_height=416,
                                   photo_size=416,
                                   protect_content=True,
                                   )

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Повторить список сказок для покупки: /start .")


async def end(update: Update) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="До свидания!")

    return ConversationHandler.END

async def help_command(update: Update) -> None:
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