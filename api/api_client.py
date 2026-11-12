"""Thin API client on top of Playwright's request context - extend with auth per project."""
from playwright.sync_api import APIResponse, Playwright


class ApiClient:
    def __init__(self, playwright: Playwright, base_url: str, headers: dict | None = None):
        # Shared headers (e.g. auth token) go here, applied to every request
        self._context = playwright.request.new_context(
            base_url=base_url,
            extra_http_headers=headers or {},
        )

    def get(self, path: str, **kwargs) -> APIResponse:
        return self._context.get(path, **kwargs)

    # Pass a dict as data= to send it as JSON
    def post(self, path: str, **kwargs) -> APIResponse:
        return self._context.post(path, **kwargs)

    def put(self, path: str, **kwargs) -> APIResponse:
        return self._context.put(path, **kwargs)

    def delete(self, path: str, **kwargs) -> APIResponse:
        return self._context.delete(path, **kwargs)

    def dispose(self):
        self._context.dispose()
