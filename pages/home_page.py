"""Demo page object for the playwright.dev home page - replace with your app's pages."""
from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    path = "/"

    def __init__(self, page: Page):
        super().__init__(page)
        # Prefer user-facing locators (role, label, text) over CSS/XPath
        self.get_started_link = page.get_by_role("link", name="Get started")

    def open_get_started(self):
        self.get_started_link.click()
