# Running tests

Run the commands from the project folder with the virtual environment activated:

```
.\.venv\Scripts\Activate.ps1      # Windows
source .venv/bin/activate         # macOS / Linux
```

Without activating, replace `pytest` with `.\.venv\Scripts\python.exe -m pytest`.

## Everything

```
pytest              # all tests, one after another
pytest -n auto      # all tests in parallel (fastest)
```

## One suite
A suite is a test file or a folder:

```
pytest tests/ui/test_home.py      # one file
pytest tests/ui                   # all UI tests
pytest tests/api                  # all API tests
```

## One test
Give the file and the test name:

```
pytest tests/ui/test_home.py::test_home_page_title
```

For one variant of a parametrized test, add its id in brackets (keep the quotes):

```
pytest "tests/ui/test_example.py::test_name[chromium-variant]"
```

To list all test names and ids: `pytest --collect-only -q`

## A group of tests

| Selection | Command |
|---|---|
| By part of the test name | `pytest -k "title or navigation"` |
| By marker (`smoke`, `regression`, `ui`, `api`) | `pytest -m smoke` or `pytest -m "regression and not api"` |
| Several specific tests | `pytest tests/ui/test_home.py::test_home_page_title tests/api/test_posts_api.py::test_get_post` |
| By Qase case ID (from `@qase.id`) | `pytest --case-ids 30,31,39` |
| Only the tests that failed last time | `pytest --lf` |

## Headless or headed
Tests run headless (no browser window) by default. Any selection above can also run in a visible browser:

```
pytest tests/ui --headed
```

To show the browser on every run, set `HEADED=true` in `.env`.

In a headed run:
- each test opens with a title card showing the test's docstring and name
- every click and entry is highlighted, with a caption of the action in the top-right corner; values typed with `BasePage.fill_secret()` are not shown
- actions are slowed down by `SLOW_MO_MS` in `.env` (500 ms by default); for one run use `--slowmo 1000`

Run headed tests without `-n auto`, otherwise several browser windows open at once.

## Other options

| Option | Effect |
|---|---|
| `-x` | stop at the first failure |
| `-v` | list each test with its result |
| `--browser firefox` | run in Firefox (install it once: `python -m playwright install firefox`) |
| `--base-url <url>` | run the UI tests against another environment |
| `--qase-mode=testops` | send this run's results to Qase |
| `--qase-testops-plan-id <id>` | run only the cases of a Qase test plan |
| `--qase-testops-run-id <id>` | add results to an existing Qase run instead of creating one |
| `--junitxml=reports/junit.xml` | JUnit XML summary, as used by the CI pipeline |

## Reports
Three outputs are available. Pick by need:

| Report | When to use it | How |
|---|---|---|
| HTML report | Every run. Quick look at what passed and failed | Always written to `reports/report.html` |
| Allure report | A richer, browsable report with history, trends and per-test details, e.g. for sharing with a team | Opt-in, see below |
| Qase TestOps | Results next to the test cases, screenshot and trace on failures, dashboards, run history in Qase | Opt-in, see README |

Failed tests always get a screenshot and a trace in `reports/artifacts/`. Replay a trace step by step with `playwright show-trace reports/artifacts/<test folder>/trace.zip`.

### Allure
The results are written only when asked for. Viewing them needs Node.js (for `npx`); the first `npx allure` call downloads the report tool.

```
pytest --alluredir=reports/allure-results                       # run with Allure results
npx allure generate reports/allure-results -o reports/allure    # build the report
npx allure open reports/allure                                  # open it in the browser
```

Results of several runs accumulate in `reports/allure-results`; delete the folder to start fresh. `--alluredir` combines with any test selection and with `-n auto`.
