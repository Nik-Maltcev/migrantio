import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Data
COUNTRIES = [
    "Австралия",
    "Австрия",
    "Албания",
    "Англия",
    "Аргентина",
    "Армения",
    "Бельгия",
    "Болгария",
    "Бразилия",
    "Венгрия",
    "Вьетнам",
    "Германия",
    "Греция",
    "Грузия",
    "Дания",
    "Египет",
    "Израиль",
    "Индия",
    "Индонезия",
    "Испания",
    "Италия",
    "Казахстан",
    "Канада",
    "Кипр",
    "Киргизия",
    "Китай",
    "Малайзия",
    "Мексика",
    "Молдова",
    "Нидерланды",
    "Новая Зеландия",
    "Норвегия",
    "ОАЭ",
    "Перу",
    "Польша",
    "Португалия",
    "Румыния",
    "США",
    "Сербия",
    "Тайланд",
    "Турция",
    "Узбекистан",
    "Филиппины",
    "Франция",
    "Чили",
    "Швеция",
    "Шри-Ланка",
    "ЮАР",
    "Южная Корея",
    "Япония"
]
CATEGORIES = [
    "Информация про страну",
    "Обмен валют",
    "Жилье",
    "Визовые вопросы",
    "Банки",
    "Комьюнити",
    "Связь",
    "Барахолка",
    "Работа",
    "Язык",
    "Куда сходить (локальные рекомендации)",
    "Laptop friendly кафе (для работы)",
    "Транспорт",
    "Медицина",
    "Семья",
    "бизнес",
    "автомобили"
]
SUBSCRIPTIONS = [
    "МЕСЯЦ 199 руб",
    "ГОД 1000",
    "ВСЕ СТРАНЫ МЕСЯЦ 490 РУБ",
    "ВСЕ СТРАНЫ ГОД 4990 РУБ"
]

# Callback data prefixes
CB_COUNTRY = "country_"
CB_CATEGORY = "cat_"
CB_BACK = "back_"
CB_MENU = "menu_"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the welcome message with the main menu."""
    text = (
        "WELCOME MESSAGE\n"
        "1 день тест план бесплатно: 1 страна на выбор"
    )
    keyboard = [
        [InlineKeyboardButton("Выбрать страну", callback_data=f"{CB_MENU}countries")],
        [InlineKeyboardButton("Купить подписку", callback_data=f"{CB_MENU}subscription")],
        [InlineKeyboardButton("Узнать что внутри", callback_data=f"{CB_MENU}info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

async def show_countries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = []
    # Create rows of 2 buttons
    row = []
    for country in COUNTRIES:
        row.append(InlineKeyboardButton(country, callback_data=f"{CB_COUNTRY}{country}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Назад", callback_data=f"{CB_MENU}start")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="СТРАНЫ",
        reply_markup=reply_markup
    )

async def show_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = []
    for sub in SUBSCRIPTIONS:
        # Assuming these buttons just show info or lead to payment (mocked for now)
        keyboard.append([InlineKeyboardButton(sub, callback_data="noop")])

    keyboard.append([InlineKeyboardButton("Назад", callback_data=f"{CB_MENU}start")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="ЦЕНЫ",
        reply_markup=reply_markup
    )

async def show_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("вернуться к списку стран", callback_data=f"{CB_MENU}countries")],
        [InlineKeyboardButton("Купить подписку", callback_data=f"{CB_MENU}subscription")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="Список того что есть",
        reply_markup=reply_markup
    )

async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    country = query.data.removeprefix(CB_COUNTRY)

    # Store selected country in context if needed, but for now just show categories

    keyboard = []
    row = []
    for cat in CATEGORIES:
        row.append(InlineKeyboardButton(cat, callback_data=f"{CB_CATEGORY}{country}|{cat}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Назад", callback_data=f"{CB_MENU}countries")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"КАТЕГОРИИ ({country})",
        reply_markup=reply_markup
    )

async def show_category_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.removeprefix(CB_CATEGORY)
    country, category = data.split("|")

    text = f"Информация по теме: {category} в стране {country}.\n\n(Текст заглушка)"

    keyboard = [[InlineKeyboardButton("Назад", callback_data=f"{CB_COUNTRY}{country}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup
    )

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == f"{CB_MENU}start":
        await start(update, context)
    elif data == f"{CB_MENU}countries":
        await show_countries(update, context)
    elif data == f"{CB_MENU}subscription":
        await show_subscription(update, context)
    elif data == f"{CB_MENU}info":
        await show_info(update, context)

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("TELEGRAM_BOT_TOKEN not set")
        return

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_menu, pattern=f"^{CB_MENU}"))
    application.add_handler(CallbackQueryHandler(show_categories, pattern=f"^{CB_COUNTRY}"))
    application.add_handler(CallbackQueryHandler(show_category_content, pattern=f"^{CB_CATEGORY}"))
    application.add_handler(CallbackQueryHandler(lambda u, c: u.callback_query.answer(), pattern="^noop$"))

    application.run_polling()

if __name__ == '__main__':
    main()
