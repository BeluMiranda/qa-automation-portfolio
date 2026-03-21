# QA Automation Portfolio


![Selenium Tests](https://github.com/BeluMiranda/qa-automation-portfolio/actions/workflows/selenium-tests.yml/badge.svg)
![API Tests](https://github.com/BeluMiranda/qa-automation-portfolio/actions/workflows/api-tests.yml/badge.svg)
![Playwright Tests](https://github.com/BeluMiranda/qa-automation-portfolio/actions/workflows/playwright-tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/BeluMiranda/qa-automation-portfolio/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/qa-automation-portfolio)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-4.18-green?logo=selenium)
![Playwright](https://img.shields.io/badge/Playwright-1.42-orange?logo=playwright)
![pytest](https://img.shields.io/badge/pytest-8.1-lightgrey?logo=pytest)
![License](https://img.shields.io/badge/license-MIT-blue)

---

> **A professional QA Automation framework** demonstrating end-to-end UI testing with Selenium & Playwright, REST API testing with pytest+requests, Page Object Model design, and fully automated CI/CD pipelines via GitHub Actions.

---

## Table of Contents

- [Tech Stack](#-tech-stack)
- [Projects](#-projects)
- [Framework Architecture](#-framework-architecture)
- [Quick Start](#-quick-start)
- [Running Tests](#-running-tests)
- [CI/CD & Reports](#-cicd--reports)
- [Documentation](#-documentation)

---

## 🛠 Tech Stack

| Category | Technology |
|---|---|
| **UI Automation** | Selenium WebDriver 4, Playwright 1.42 |
| **API Testing** | requests, httpx, pytest |
| **Language** | Python 3.11 |
| **Test Framework** | pytest 8 + plugins |
| **Reporting** | Allure Reports, pytest-html, Codecov |
| **CI/CD** | GitHub Actions |
| **Design Pattern** | Page Object Model (POM) |

---

## 📁 Projects

### 1. 🛒 Selenium E2E — Sauce Demo
End-to-end test suite for [saucedemo.com](https://www.saucedemo.com) — a public e-commerce demo.

| Suite | Tests | Markers |
|---|---|---|
| Login | 10 | smoke, regression |
| Inventory & Sorting | 12 | smoke, regression |
| Cart & Checkout (E2E) | 6 | smoke, regression |

**Highlights:**
- Full Page Object Model with `BasePage` inheritance
- Screenshot attachment on failure (via Allure)
- Security test: SQL injection on login form
- Data-driven with JSON fixtures

---

### 2. 🔌 API Testing — JSONPlaceholder & ReqRes
REST API validation suite using two public APIs.

| Suite | Tests | API |
|---|---|---|
| Posts (CRUD) | 10 | jsonplaceholder.typicode.com |
| Users & Pagination | 10 | jsonplaceholder + reqres.in |

**Highlights:**
- Reusable `APIClient` with automatic retries and logging
- Schema validation on response bodies
- Response time assertions
- CRUD: GET, POST, PUT, PATCH, DELETE

---

### 3. 🎭 Playwright — Multi-browser
Same Sauce Demo scenarios re-implemented with Playwright.

| Suite | Tests | Browsers |
|---|---|---|
| Login | 5 | chromium, firefox |
| Inventory | 3 | chromium, firefox |

**Highlights:**
- Demonstrates auto-waiting (no `time.sleep`)
- `authenticated_page` fixture for pre-login state
- Uses `expect()` for Playwright-native assertions
- Runs on Chromium AND Firefox in CI in parallel

---

## 🏗 Framework Architecture

```
.
├── tests/
│   ├── selenium_tests/
│   │   ├── pages/          ← Page Object classes
│   │   ├── tests/          ← Test classes
│   │   ├── fixtures/       ← Test data (JSON)
│   │   └── conftest.py     ← WebDriver fixture
│   ├── api_tests/
│   │   ├── helpers/        ← APIClient
│   │   ├── tests/          ← Test classes
│   │   ├── fixtures/       ← Payloads (JSON)
│   │   └── conftest.py     ← Client fixtures
│   └── playwright_tests/
│       ├── pages/          ← Page Object classes
│       ├── tests/          ← Test classes
│       └── conftest.py     ← Browser + auth fixtures
├── utils/
│   ├── config.py           ← Centralised settings
│   └── logger.py           ← Structured JSON logger
├── .github/
│   ├── workflows/          ← GitHub Actions pipelines
│   └── ISSUE_TEMPLATE/     ← Bug & test case templates
└── documentation/          ← Test plan, architecture, best practices
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Google Chrome (latest)
- Git

### 1. Clone the repository
```bash
git clone https://github.com/BeluMiranda/qa-automation-portfolio.git
cd qa-automation-portfolio
```

### 2. Create a virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers
```bash
playwright install chromium firefox
```

### 5. Configure environment
```bash
cp .env.example .env
# Edit .env if needed (defaults work for all public test sites)
```

---

## ▶️ Running Tests

### All tests
```bash
pytest tests/ -v
```

### By suite
```bash
# Selenium only
pytest tests/selenium_tests/tests/ -v

# API only
pytest tests/api_tests/tests/ -v

# Playwright only
pytest tests/playwright_tests/tests/ -v
```

### By marker
```bash
pytest tests/ -m smoke          # ~5 minutes
pytest tests/ -m regression     # full suite
pytest tests/ -m api            # API suite only
pytest tests/ -m playwright     # Playwright suite only
```

### With Allure report (local)
```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### Run headful (visible browser — for debugging)
```bash
HEADLESS=false pytest tests/selenium_tests/tests/test_login.py -v
```

---

## ⚙️ CI/CD & Reports

### Pipelines

| Workflow | Trigger | Browsers |
|---|---|---|
| Selenium Tests | push, PR, daily 08:00 UTC | Chrome |
| API Tests | push, PR, daily 08:30 UTC | N/A |
| Playwright Tests | push, PR, daily 09:00 UTC | Chromium + Firefox |
| Allure Report | after any test workflow | N/A |

### Live Allure Report
📊 **[View Latest Report](https://BeluMiranda.github.io/qa-automation-portfolio/)**

_(Available after pushing to `main` and GitHub Actions completes)_

---

## 📚 Documentation

| Document | Description |
|---|---|
| [Test Plan](documentation/TEST_PLAN.md) | Strategy, scope, entry/exit criteria |
| [Architecture](documentation/ARCHITECTURE.md) | Framework design and decisions |
| [Best Practices](documentation/BEST_PRACTICES.md) | Coding standards and patterns |

---

## 📋 Test Summary

| Suite | Tests | Smoke | Regression |
|---|---|---|---|
| Selenium — Login | 10 | 3 | 7 |
| Selenium — Inventory | 12 | 4 | 8 |
| Selenium — Checkout | 6 | 2 | 4 |
| API — Posts | 10 | 3 | 7 |
| API — Users | 10 | 4 | 6 |
| Playwright — Login | 5 | 1 | 4 |
| Playwright — Inventory | 3 | 2 | 1 |
| **Total** | **56** | **19** | **37** |

---

## 📄 License

MIT © Belen Miranda
