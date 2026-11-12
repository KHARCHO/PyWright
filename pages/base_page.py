"""Base class for all page objects - keep only logic shared by every page here."""
from playwright.sync_api import Locator, Page


class BasePage:
    # Page path relative to BASE_URL, override in each page object
    path = "/"
    # Set by the page fixture in headed runs (action captions on screen)
    action_captions = False

    def __init__(self, page: Page):
        self.page = page

    # wait_until="domcontentloaded" is faster when the full page load isn't needed
    def open(self, wait_until: str = "load"):
        self.page.goto(self.path, wait_until=wait_until)
        return self

    def fill_secret(self, field: Locator, value: str):
        # Keeps passwords and tokens out of the on-screen action captions
        if not self.action_captions:
            field.fill(value)
            return
        self.page.screencast.hide_actions()
        field.fill(value)
        self.page.screencast.show_actions()
