import pytest
from unittest.mock import patch, mock_open


@pytest.fixture(autouse=True)
def _set_env_vars(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "test_token")
    monkeypatch.setenv("ADMIN_ID", "12345")


def test_bots_dataclass():
    from core.settings import Bots
    bot = Bots(bot_token="token", admin_id="1")
    assert bot.bot_token == "token"
    assert bot.admin_id == "1"


def test_settings_dataclass():
    from core.settings import Bots, Settings
    bots = Bots(bot_token="t", admin_id="a")
    settings = Settings(bots=bots)
    assert settings.bots.bot_token == "t"


def test_get_settings_from_env():
    from core.settings import Bots, Settings, get_settings
    result = get_settings()
    assert isinstance(result, Settings)
    assert isinstance(result.bots, Bots)


def test_get_settings_from_file():
    from core.settings import Bots, Settings, get_settings
    with (
        patch("os.path.isfile", return_value=True),
        patch("core.settings.Env.read_env"),
        patch("builtins.open", mock_open(read_data="BOT_TOKEN=abc\nADMIN_ID=1\n")),
    ):
        result = get_settings(".env")
        assert isinstance(result, Settings)
        assert isinstance(result.bots, Bots)
