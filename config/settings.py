"""Central test settings, read from environment variables and the local .env file."""
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent

# Real environment variables win over .env, so CI can override anything
load_dotenv(ROOT_DIR / ".env")


def _env(name: str, default: str = "") -> str:
    return os.getenv(name) or default


@dataclass(frozen=True)
class Settings:
    base_url: str = _env("BASE_URL", "https://playwright.dev")
    api_base_url: str = _env("API_BASE_URL", "https://jsonplaceholder.typicode.com")
    default_timeout_ms: int = int(_env("DEFAULT_TIMEOUT_MS", "10000"))
    # Show the browser window; headless by default
    headed: bool = _env("HEADED", "false").lower() == "true"
    # Pause between actions in headed runs so they can be followed
    slow_mo_ms: int = int(_env("SLOW_MO_MS", "500"))
    # Scripts stubbed out in the browser, e.g. chat widgets that hang page load
    blocked_urls: tuple = tuple(u.strip() for u in _env("BLOCKED_URLS").split(",") if u.strip())
    # Test user for login flows - keep real values only in local .env
    app_username: str = _env("APP_USERNAME")
    app_password: str = _env("APP_PASSWORD")


settings = Settings()
