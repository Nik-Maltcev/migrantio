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
    "Медицина"
]
SUBSCRIPTIONS = [
    "МЕСЯЦ 199 руб",
    "ГОД 1000",
    "ВСЕ СТРАНЫ МЕСЯЦ 490 РУБ",
    "ВСЕ СТРАНЫ ГОД 4990 РУБ"
]

CITIES = {
    "США": ["Нью-Йорк", "Лос-Анджелес", "Чикаго", "Хьюстон", "Финикс", "Филадельфия", "Сан-Антонио", "Сан-Диего", "Даллас", "Сан-Хосе"],
    "Турция": ["Стамбул", "Анкара", "Измир", "Бурса", "Анталья", "Адана", "Конья", "Шанлыурфа", "Газиантеп", "Мерсин"],
    "Тайланд": ["Бангкок", "Пхукет", "Чиангмай", "Паттайя", "Краби", "Самуи", "Хуахин", "Хатъяй", "Удонтхани", "Накхонратчасима"],
    "Казахстан": ["Алматы", "Астана", "Шымкент", "Актобе", "Караганда", "Тараз", "Усть-Каменогорск", "Павлодар", "Атырау", "Семей"],
    "Германия": ["Берлин", "Гамбург", "Мюнхен", "Кельн", "Франкфурт", "Штутгарт", "Дюссельдорф", "Дортмунд", "Эссен", "Лейпциг"],
    "Франция": ["Париж", "Марсель", "Лион", "Тулуза", "Ницца", "Нант", "Страсбург", "Монпелье", "Бордо", "Лилль"],
    "Испания": ["Мадрид", "Барселона", "Валенсия", "Севилья", "Сарагоса", "Малага", "Мурсия", "Пальма", "Лас-Пальмас", "Бильбао"],
    "Италия": ["Рим", "Милан", "Неаполь", "Турин", "Палермо", "Генуя", "Болонья", "Флоренция", "Бари", "Катания"],
    "Индонезия": ["Джакарта", "Сурабая", "Бандунг", "Медан", "Бали", "Семаранг", "Макасар", "Палембанг", "Тангеранг", "Депок"],
    "Грузия": ["Тбилиси", "Батуми", "Кутаиси", "Рустави", "Гори", "Зугдиди", "Поти", "Хашури", "Самтредиа", "Сенаки"],
    "Армения": ["Ереван", "Гюмри", "Ванадзор", "Вагаршапат", "Абовян", "Капан", "Раздан", "Армавир", "Арташат", "Иджеван"],
    "Сербия": ["Белград", "Нови-Сад", "Ниш", "Крагуевац", "Суботица", "Зренянин", "Панчево", "Чачак", "Крушевац", "Кралево"]
}

# Callback data prefixes
CB_COUNTRY = "country_"
CB_CITY = "city_"
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

async def show_cities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    country = query.data.removeprefix(CB_COUNTRY)

    # Store country in user_data
    context.user_data['country'] = country

    cities = CITIES.get(country, [])

    keyboard = []
    row = []
    for city in cities:
        row.append(InlineKeyboardButton(city, callback_data=f"{CB_CITY}{city}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # Add "All cities" option
    keyboard.append([InlineKeyboardButton("Все города", callback_data=f"{CB_CITY}Все города")])
    keyboard.append([InlineKeyboardButton("Назад", callback_data=f"{CB_MENU}countries")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"ГОРОДА ({country})",
        reply_markup=reply_markup
    )

async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    city = query.data.removeprefix(CB_CITY)
    context.user_data['city'] = city

    country = context.user_data.get('country', 'Unknown')

    keyboard = []
    row = []
    for cat in CATEGORIES:
        # Pass only category, rely on user_data for context
        row.append(InlineKeyboardButton(cat, callback_data=f"{CB_CATEGORY}{cat}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # Back button goes to show_cities, which needs CB_COUNTRY + country
    keyboard.append([InlineKeyboardButton("Назад", callback_data=f"{CB_COUNTRY}{country}")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"КАТЕГОРИИ ({country}, {city})",
        reply_markup=reply_markup
    )

async def show_category_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data.removeprefix(CB_CATEGORY)

    country = context.user_data.get('country', 'Unknown')
    city = context.user_data.get('city', 'Unknown')

    text = f"Информация по теме: {category} в стране {country}, город {city}.\n\n(Текст заглушка)"

    # Back button goes to show_categories, which needs CB_CITY + city
    keyboard = [[InlineKeyboardButton("Назад", callback_data=f"{CB_CITY}{city}")]]
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
    application.add_handler(CallbackQueryHandler(show_cities, pattern=f"^{CB_COUNTRY}"))
    application.add_handler(CallbackQueryHandler(show_categories, pattern=f"^{CB_CITY}"))
    application.add_handler(CallbackQueryHandler(show_category_content, pattern=f"^{CB_CATEGORY}"))
    application.add_handler(CallbackQueryHandler(lambda u, c: u.callback_query.answer(), pattern="^noop$"))

    application.run_polling()

if __name__ == '__main__':
    main()
