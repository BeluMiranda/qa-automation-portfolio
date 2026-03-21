# Architecture — QA Automation Framework

## Overview

This framework follows a **layered architecture** that separates test logic, page interactions,
data management, utilities, and CI/CD configuration.

---

## Directory Structure

```
qa-automation-portfolio/
│
├── .github/                        # CI/CD & GitHub configuration
│   ├── workflows/                  # GitHub Actions pipelines
│   │   ├── selenium-tests.yml      # Selenium regression pipeline
│   │   ├── api-tests.yml           # API test pipeline
│   │   ├── playwright-tests.yml    # Playwright multi-browser pipeline
│   │   └── allure-report.yml       # Allure → GitHub Pages publisher
│   └── ISSUE_TEMPLATE/             # Standardized issue forms
│
├── tests/
│   ├── selenium_tests/
│   │   ├── conftest.py             # WebDriver fixtures (scope: function)
│   │   ├── pages/                  # Page Object Model classes
│   │   │   ├── base_page.py        # Abstract base with common interactions
│   │   │   ├── login_page.py       # /  — Login page
│   │   │   ├── inventory_page.py   # /inventory.html
│   │   │   └── cart_page.py        # /cart + checkout pages
│   │   ├── tests/                  # Test classes
│   │   │   ├── test_login.py       # 10 login scenarios
│   │   │   ├── test_inventory.py   # 12 inventory/sorting/cart scenarios
│   │   │   └── test_checkout.py    # 6 checkout E2E scenarios
│   │   └── fixtures/
│   │       └── users.json          # Credentials and test data
│   │
│   ├── api_tests/
│   │   ├── conftest.py             # Session-scoped API clients
│   │   ├── helpers/
│   │   │   └── api_client.py       # Reusable HTTP client + assertions
│   │   ├── tests/
│   │   │   ├── test_posts.py       # 10 POST resource scenarios (JSONPlaceholder)
│   │   │   └── test_users.py       # 10 User scenarios (JSONPlaceholder + ReqRes)
│   │   └── fixtures/
│   │       └── payloads.json       # Request body data
│   │
│   └── playwright_tests/
│       ├── conftest.py             # Playwright fixtures + auth helper
│       ├── pages/                  # POM classes (Playwright)
│       │   ├── base_page.py
│       │   ├── login_page.py
│       │   └── inventory_page.py
│       └── tests/
│           └── test_saucedemo.py   # Login + Inventory Playwright tests
│
├── utils/
│   ├── config.py                   # Centralised Settings (dataclasses + .env)
│   └── logger.py                   # JSON structured logger
│
├── documentation/
│   ├── TEST_PLAN.md
│   ├── TEST_CASES.md
│   ├── ARCHITECTURE.md             ← this file
│   └── BEST_PRACTICES.md
│
├── reports/                        # Generated artifacts (gitignored except .gitkeep)
├── .env.example                    # Environment template
├── pytest.ini                      # pytest configuration
├── requirements.txt                # Python dependencies
└── README.md
```

---

## Design Patterns

### Page Object Model (POM)

```
Test Class
    │  uses
    ▼
Page Object  ──► BasePage (common interactions)
    │  uses
    ▼
WebDriver / Playwright Page API
```

- Each page class has **locators** (private) and **actions/getters** (public)
- Tests never interact with locators directly
- One class per application page

### Fixture Hierarchy

```
session scope ── API clients (created once per test session)
    │
function scope ── WebDriver (new browser per test for isolation)
    │
autouse fixture ── Page navigation setup (load URL before each test)
```

### Data-Driven Approach

```
tests/*/fixtures/*.json
        │
        ▼
json.loads() in test file
        │
        ▼
Parametrize OR direct dict access
```

---

## CI/CD Pipeline Flow

```
Developer pushes to main/develop
            │
            ▼
GitHub Actions triggered (3 parallel jobs)
   ┌─────────────┬──────────────┬─────────────┐
   │  Selenium   │  API Tests   │ Playwright  │
   │  (Chrome)   │  (pytest)    │ (chromium + │
   │             │              │  firefox)   │
   └─────┬───────┴──────┬───────┴──────┬──────┘
         │              │              │
         ▼              ▼              ▼
   allure-results  allure-results  allure-results
         │              │              │
         └──────────────┴──────────────┘
                        │
                        ▼
              Allure Report Workflow
                        │
                        ▼
             GitHub Pages (gh-pages branch)
             https://your-user.github.io/qa-automation-portfolio/
```

---

## Key Decisions

| Decision | Rationale |
|---|---|
| pytest over unittest | Simpler syntax, powerful fixtures, rich plugin ecosystem |
| POM pattern | Reduces duplication, locators in one place, easier maintenance |
| Session-scoped API clients | Avoids creating HTTP sessions per test (performance) |
| Function-scoped WebDriver | Test isolation — one browser per test, no shared state |
| JSON fixtures over hardcoded data | Test data visible and editable without modifying test logic |
| Allure over pytest-html only | Richer reports, timeline, steps, screenshots, history |
