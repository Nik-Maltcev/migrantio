import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, User, Message, CallbackQuery, Chat
from src.bot import (
    start,
    show_countries,
    show_cities,
    show_subscription,
    show_info,
    show_categories,
    show_category_content,
    handle_menu,
    CB_MENU,
    CB_COUNTRY,
    CB_CITY,
    CB_CATEGORY
)

@pytest.fixture
def update():
    update = MagicMock(spec=Update)
    update.effective_user = MagicMock(spec=User)
    update.effective_user.id = 123
    update.effective_chat = MagicMock(spec=Chat)
    update.effective_chat.id = 123
    return update

@pytest.fixture
def context():
    context = MagicMock()
    context.user_data = {}
    return context

@pytest.mark.asyncio
async def test_start_command(update, context):
    update.callback_query = None
    update.message = AsyncMock(spec=Message)

    await start(update, context)

    update.message.reply_text.assert_called_once()
    args, kwargs = update.message.reply_text.call_args
    assert "WELCOME MESSAGE" in kwargs['text']
    assert kwargs['reply_markup'].inline_keyboard is not None

@pytest.mark.asyncio
async def test_start_callback(update, context):
    update.callback_query = AsyncMock(spec=CallbackQuery)
    update.message = None

    await start(update, context)

    update.callback_query.edit_message_text.assert_called_once()
    args, kwargs = update.callback_query.edit_message_text.call_args
    assert "WELCOME MESSAGE" in kwargs['text']

@pytest.mark.asyncio
async def test_show_countries(update, context):
    update.callback_query = AsyncMock(spec=CallbackQuery)

    await show_countries(update, context)

    update.callback_query.edit_message_text.assert_called_once()
    args, kwargs = update.callback_query.edit_message_text.call_args
    assert "СТРАНЫ" == kwargs['text']
    # Check if countries are in the keyboard
    buttons = [btn.text for row in kwargs['reply_markup'].inline_keyboard for btn in row]
    assert "Италия" in buttons
    assert "Испания" in buttons

@pytest.mark.asyncio
async def test_show_cities(update, context):
    update.callback_query = AsyncMock(spec=CallbackQuery)
    update.callback_query.data = f"{CB_COUNTRY}Италия"

    await show_cities(update, context)

    update.callback_query.edit_message_text.assert_called_once()
    args, kwargs = update.callback_query.edit_message_text.call_args
    assert "ГОРОДА (Италия)" == kwargs['text']

    # Check that context was updated
    assert context.user_data['country'] == "Италия"

    buttons = [btn.text for row in kwargs['reply_markup'].inline_keyboard for btn in row]
    assert "Рим" in buttons
    assert "Все города" in buttons

@pytest.mark.asyncio
async def test_show_categories(update, context):
    update.callback_query = AsyncMock(spec=CallbackQuery)
    context.user_data['country'] = "Италия"
    # Callback format: city_CityName
    update.callback_query.data = f"{CB_CITY}Рим"

    await show_categories(update, context)

    update.callback_query.edit_message_text.assert_called_once()
    args, kwargs = update.callback_query.edit_message_text.call_args
    assert "КАТЕГОРИИ (Италия, Рим)" == kwargs['text']

    assert context.user_data['city'] == "Рим"

    # Check if categories are in the keyboard
    buttons = [btn.text for row in kwargs['reply_markup'].inline_keyboard for btn in row]
    assert "Информация про страну" in buttons
    assert "Визовые вопросы" in buttons

@pytest.mark.asyncio
async def test_show_category_content(update, context):
    update.callback_query = AsyncMock(spec=CallbackQuery)
    context.user_data['country'] = "Италия"
    context.user_data['city'] = "Рим"
    # Callback format: cat_<ID> where ID is numeric
    # "Визовые вопросы" is at index 3
    update.callback_query.data = f"{CB_CATEGORY}3"

    await show_category_content(update, context)

    update.callback_query.edit_message_text.assert_called_once()
    args, kwargs = update.callback_query.edit_message_text.call_args
    assert "Информация по теме: Визовые вопросы в стране Италия, город Рим." in kwargs['text']

@pytest.mark.asyncio
async def test_handle_menu_countries(update, context):
    update.callback_query = AsyncMock(spec=CallbackQuery)
    update.callback_query.data = f"{CB_MENU}countries"

    await handle_menu(update, context)

    # Should call show_countries, which edits message
    update.callback_query.edit_message_text.assert_called_once()
    args, kwargs = update.callback_query.edit_message_text.call_args
    assert "СТРАНЫ" == kwargs['text']
