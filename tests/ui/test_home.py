"""Demo UI tests against playwright.dev - use as a pattern for real test cases."""
import re

import pytest
from playwright.sync_api import Page, expect
from qase.pytest import qase

from pages.home_page import HomePage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
@qase.title("Home page opens with correct title")
def test_home_page_title(page: Page):
    HomePage(page).open()
    expect(page).to_have_title(re.compile("Playwright"))


@pytest.mark.regression
@qase.title("Get started link leads to installation docs")
def test_get_started_navigation(page: Page):
    home = HomePage(page)

    # Steps show up in the Qase result when reporting is on
    with qase.step("Open home page"):
        home.open()
    with qase.step("Click 'Get started'"):
        home.open_get_started()
    with qase.step("Installation docs are shown"):
        expect(page).to_have_url(re.compile(r"/docs/intro"))
        expect(page.get_by_role("heading", name="Installation")).to_be_visible()
