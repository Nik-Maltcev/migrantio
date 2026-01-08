import pytest
from src.bot import COUNTRIES

def test_countries_sorted():
    sorted_countries = sorted(COUNTRIES)
    assert COUNTRIES == sorted_countries, "Countries list is not sorted alphabetically"

def test_countries_content():
    expected_countries = [
        "Австралия", "Австрия", "Албания", "Англия", "Аргентина", "Армения",
        "Бельгия", "Болгария", "Бразилия", "Венгрия", "Вьетнам", "Германия",
        "Греция", "Грузия", "Дания", "Египет", "Израиль", "Индия", "Индонезия",
        "Испания", "Италия", "Казахстан", "Канада", "Кипр", "Киргизия", "Китай",
        "Малайзия", "Мексика", "Молдова", "Нидерланды", "Новая Зеландия",
        "Норвегия", "ОАЭ", "Перу", "Польша", "Португалия", "Румыния", "США",
        "Сербия", "Тайланд", "Турция", "Узбекистан", "Филиппины", "Франция",
        "Чили", "Швеция", "Шри-Ланка", "ЮАР", "Южная Корея", "Япония"
    ]
    # Check if all expected countries are in COUNTRIES
    for country in expected_countries:
        assert country in COUNTRIES, f"{country} is missing from COUNTRIES"

    # Check if there are no extra countries
    assert len(COUNTRIES) == len(expected_countries), "COUNTRIES list has unexpected length"
