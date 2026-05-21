from core.keyboards.reply import get_reply_keyboard
from core.keyboards.inline import get_inline_keyboard


def test_reply_keyboard_returns_markup():
    markup = get_reply_keyboard()
    assert markup is not None


def test_inline_keyboard_returns_markup():
    markup = get_inline_keyboard()
    assert markup is not None


def test_reply_keyboard_has_expected_buttons():
    markup = get_reply_keyboard()
    keyboard = markup.keyboard
    all_buttons = [btn.text for row in keyboard for btn in row]
    assert "FAQ" in all_buttons
    assert "Заказать бот" in all_buttons


def test_inline_keyboard_has_expected_buttons():
    markup = get_inline_keyboard()
    keyboard = markup.inline_keyboard
    all_buttons = [btn.text for row in keyboard for btn in row]
    assert "Написать разработчикам" in all_buttons
