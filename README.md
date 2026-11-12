# PyWright

Test automation template for web applications with Python, Playwright and pytest. It has a Page Object UI layer, an API layer and optional reporting to Qase TestOps.

## Setup on a new PC
Nothing is compiled. Each PC needs a one-time setup that creates a local virtual environment (`.venv`) and downloads the browser. `.venv`, `.env` and `reports/` are local to each PC and are not copied or committed.

1. Install Python 3.10+ from [python.org](https://www.python.org/downloads/). On Windows, tick "Add python.exe to PATH", then check `python --version` in a new terminal.
2. Clone the repository, or copy the folder without `.venv`, `.env` and `reports`.
3. Run the setup from the project folder (takes a few minutes, can be re-run):
   ```
   .\setup.ps1      # Windows
   ./setup.sh       # macOS / Linux
   ```
   It creates `.venv`, installs the pinned packages and Chromium, and creates `.env` from `.env.example`.
   If PowerShell blocks the script: `powershell -ExecutionPolicy Bypass -File .\setup.ps1`
4. Fill in `.env`:
   - `BASE_URL` of the application, and `BLOCKED_URLS` if needed
   - the test account: `APP_USERNAME` and `APP_PASSWORD`
   - for Qase: `QASE_MODE=testops`, `QASE_TESTOPS_PROJECT` and `QASE_TESTOPS_API_TOKEN`
5. Run the tests and open `reports/report.html`.

After pulling new code, re-run the setup if `requirements.txt` changed.

## Running tests
[RUNNING_TESTS.md](RUNNING_TESTS.md) covers running everything, one suite, one test or a group of tests, headless or headed. The most common commands, with the venv activated:

```
pytest -n auto                    # everything, in parallel
pytest tests/ui/test_home.py      # one suite
pytest -k title --headed          # selected tests in a visible browser
```

Results of the last run are in `reports/report.html`; an Allure report and Qase reporting are available as options (see the guide and the Qase section).

## Structure
```
config/settings.py   settings from .env
pages/               page objects, based on BasePage
api/api_client.py    API client on Playwright's request context
tests/conftest.py    shared fixtures
tests/ui/            UI tests
tests/api/           API tests
pytest.ini           markers and default options
qase.config.json     Qase reporter settings
ruff.toml            linter rules
.gitlab-ci.yml       GitLab pipeline (on demand)
.github/workflows/   GitHub Actions pipeline (on demand)
```

## Fixtures and helpers
- `BLOCKED_URLS` in `.env`: comma-separated URL patterns answered with an empty response, for third-party scripts (chat widgets, ads) that hang the page load or cover elements.
- `js_errors`: uncaught JavaScript and console errors collected during a test. Clear it after the page loads to check only your own actions.
- `user_credentials`: `(login, password)` from `APP_USERNAME` / `APP_PASSWORD`. The test is skipped when they are not set. A signed-in test asks for the fixture, signs in through its login page object and continues on the same page.
- `BasePage.open(wait_until="domcontentloaded")`: faster navigation when the full page load is not needed.
- `BasePage.fill_secret(field, value)`: types a password or token without showing it in the action captions of headed runs.
- Tests on open bugs fail like any other; note the bug ID in a comment above the test so the failure is understood at a glance.

## Starting a new project
1. Set `BASE_URL`, `API_BASE_URL`, the test account and any `BLOCKED_URLS` in `.env`, and the same keys without secrets in `.env.example`.
2. Add page objects to `pages/`, with locators as attributes and user actions as methods.
3. Add tests under `tests/ui/` or `tests/api/` and mark them `smoke` or `regression`.
4. Remove the demo files: `home_page.py`, `test_home.py`, `test_posts_api.py`.

## Qase reporting
Reporting uses [qase-pytest](https://github.com/qase-tms/qase-python/tree/main/qase-pytest) and is off by default.

1. In Qase, copy the project code and create an API token.
2. Set the project code in `qase.config.json` or as `QASE_TESTOPS_PROJECT` in `.env`.
3. In `.env`, set `QASE_MODE=testops` and `QASE_TESTOPS_API_TOKEN`, or pass `--qase-mode=testops` for a single run.
4. Link tests to Qase cases with `@qase.id(<case id>)`, add steps with `with qase.step(...)`, and keep a test out of reporting with `@qase.ignore()`.

Results are pushed from the machine running the tests: each run creates a completed test run named "PyWright automated run <date> <time>" (set `QASE_TESTOPS_RUN_TITLE` in `.env` for another name). `--qase-testops-plan-id <id>` limits a run to the cases of a Qase test plan. A failed UI result carries a screenshot of the page and the Playwright trace. Settings are applied in this order: CLI, environment / `.env`, `qase.config.json`.

## Code style and CI
`ruff check .` lints the code (rules in `ruff.toml`); `ruff check --fix .` applies the safe fixes.

The pipeline runs the linter, then the suite, with reports and failure artifacts kept for two weeks. It is defined for both hosts and starts on demand or on a schedule, not on every push, so local runs stay the default:

| Host | File | Start a run | Variables |
|---|---|---|---|
| GitLab | `.gitlab-ci.yml` | CI/CD > Pipelines > Run pipeline | Settings > CI/CD > Variables |
| GitHub | `.github/workflows/tests.yml` | Actions > Tests > Run workflow | Settings > Secrets and variables > Actions |

Before the first run, add the `.env` values there: `APP_USERNAME`, `APP_PASSWORD`, and for Qase `QASE_MODE=testops`, `QASE_TESTOPS_PROJECT` and `QASE_TESTOPS_API_TOKEN` (on GitHub, tokens and passwords as secrets, the rest as variables).

## Troubleshooting
| Problem | Fix |
|---|---|
| `python` is not recognized | Reinstall Python with "Add python.exe to PATH" and open a new terminal |
| `Activate.ps1` cannot be loaded | Run `.\.venv\Scripts\python.exe -m pytest` instead |
| Browser executable is missing | `.\.venv\Scripts\python.exe -m playwright install chromium` |
| Signed-in tests are skipped | Set `APP_USERNAME` and `APP_PASSWORD` in `.env` |
| Pages hang for about 30 s | A third-party script never loads: add its URL pattern to `BLOCKED_URLS` |
