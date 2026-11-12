"""Shared fixtures for UI and API tests."""
import os
import sys
from datetime import datetime
from pathlib import Path

import pytest
from qase.pytest import qase
from qase.pytest.plugin import QasePytestPlugin

from api.api_client import ApiClient
from config.settings import settings
from pages.base_page import BasePage

# qase-pytest calls `pip show`: resolve it to this venv even when it is not activated
os.environ["PATH"] = os.pathsep.join([str(Path(sys.executable).parent), os.environ.get("PATH", "")])
# Date the Qase run title to tell runs apart; QASE_TESTOPS_RUN_TITLE in .env still wins
os.environ.setdefault("QASE_TESTOPS_RUN_TITLE", f"PyWright automated run {datetime.now():%Y-%m-%d %H:%M}")


def pytest_addoption(parser):
    parser.addoption("--case-ids", help="run only tests linked to these Qase case IDs, e.g. 30,31,39")


def pytest_collection_modifyitems(config, items):
    wanted = config.getoption("--case-ids")
    if not wanted:
        return
    ids = {int(i) for i in wanted.split(",")}
    keep = [item for item in items if ids & set(QasePytestPlugin.get_qase_ids(item) or [])]
    config.hook.pytest_deselected(items=[item for item in items if item not in keep])
    items[:] = keep


@pytest.fixture(scope="session")
def base_url(request):
    # CLI --base-url overrides .env
    return request.config.getoption("base_url") or settings.base_url


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    # HEADED=true in .env shows the browser; --headed on the CLI works as well
    args = {**browser_type_launch_args, "headless": False} if settings.headed else browser_type_launch_args
    if args.get("headless") is False:
        # Slow visible runs down so they can be followed; --slowmo on the CLI wins
        args = {"slow_mo": settings.slow_mo_ms, **args}
    return args


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    # Default desktop viewport; --device emulation still takes priority
    return {"viewport": {"width": 1920, "height": 1080}, **browser_context_args}


@pytest.fixture
def context(context):
    # Empty 200 instead of abort, so blocked scripts don't add console errors
    for pattern in settings.blocked_urls:
        context.route(pattern, lambda route: route.fulfill(status=200, body=""))
    return context


@pytest.fixture
def page(page, request, browser_type_launch_args):
    page.set_default_timeout(settings.default_timeout_ms)
    if browser_type_launch_args.get("headless") is False:
        # Headed runs: title card per test, captions on every action
        BasePage.action_captions = True
        page.screencast.show_actions()
        title = (request.function.__doc__ or request.node.name).strip().splitlines()[0]
        page.screencast.show_chapter(title, description=request.node.nodeid, duration=1500)
    yield page
    # Failed test: the page as it was left goes to the Qase result (rep_call is set by pytest-playwright)
    failed = getattr(request.node, "rep_call", None) is not None and request.node.rep_call.failed
    if failed and request.config.qase.config.mode.value != "off" and not page.is_closed():
        qase.attach((page.screenshot(), "image/png", "failure.png"))


@pytest.fixture
def js_errors(page):
    """Uncaught page errors and console errors collected while the test runs."""
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    return errors


@pytest.fixture
def user_credentials():
    """Existing account from .env; signed-in tests skip when it is not set."""
    if not (settings.app_username and settings.app_password):
        pytest.skip("Set APP_USERNAME and APP_PASSWORD in .env to run signed-in tests")
    return settings.app_username, settings.app_password


@pytest.fixture(scope="session")
def api(playwright):
    client = ApiClient(playwright, settings.api_base_url)
    yield client
    client.dispose()
