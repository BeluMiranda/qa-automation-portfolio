# Test Plan — QA Automation Portfolio

## 1. Introduction

This document describes the automated testing strategy for the QA Automation Portfolio project.
All tests target publicly available demo applications to showcase real-world automation skills.

---

## 2. Scope

### In Scope
| Application | URL | Test Types |
|---|---|---|
| Sauce Demo (e-commerce) | https://www.saucedemo.com | UI / E2E |
| JSONPlaceholder (Blog API) | https://jsonplaceholder.typicode.com | API / REST |
| ReqRes (Users API) | https://reqres.in | API / REST |

### Out of Scope
- Performance/load testing
- Security penetration testing
- Mobile testing

---

## 3. Test Strategy

### 3.1 Testing Pyramid

```
        /\
       /E2E\          ← Fewer, slower, high value
      /------\
     /  API   \       ← Medium quantity, fast
    /----------\
   / Unit/Comp  \     ← Many, fastest (future)
  /--------------\
```

### 3.2 Frameworks

| Framework | Language | Use Case |
|---|---|---|
| Selenium WebDriver | Python | Cross-browser E2E testing |
| Playwright | Python | Modern E2E / multi-browser |
| pytest + requests | Python | REST API testing |

### 3.3 Design Patterns

- **Page Object Model (POM)**: All UI interactions encapsulated in page classes
- **Fixture-based setup**: pytest fixtures for driver/client lifecycle
- **Data-driven testing**: Test data separated in JSON fixtures
- **AAA pattern**: Arrange — Act — Assert in every test

---

## 4. Test Environment

### Local
```
OS: Windows 11 / Ubuntu 22.04
Python: 3.11+
Browser: Chrome (latest stable)
```

### CI/CD
```
Platform: GitHub Actions
Runner: ubuntu-latest
Browser: Chrome (headless), Firefox (headless)
Trigger: Push to main/develop, Pull Request, daily schedule
```

---

## 5. Test Execution

### Run all tests
```bash
pytest tests/ -v
```

### Run by marker
```bash
pytest tests/ -m smoke          # Quick sanity check
pytest tests/ -m regression     # Full regression suite
pytest tests/ -m api            # API tests only
pytest tests/ -m playwright     # Playwright tests only
```

### Run with Allure report
```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### Run Selenium only
```bash
pytest tests/selenium_tests/tests/ -v
```

### Run API only
```bash
pytest tests/api_tests/tests/ -v
```

---

## 6. Entry / Exit Criteria

### Entry Criteria
- Application under test is accessible and stable
- All dependencies installed (`pip install -r requirements.txt`)
- Environment variables configured (`.env`)

### Exit Criteria
- All SMOKE tests pass ✅
- No BLOCKER/CRITICAL test failures in regression suite
- Test report generated and published

---

## 7. Defect Management

Defects are tracked via **GitHub Issues** using the Bug Report template.
Labels: `bug`, `needs-triage`, `in-progress`, `resolved`

---

## 8. Reporting

| Report Type | Tool | Location |
|---|---|---|
| HTML Report | pytest-html | `reports/*.html` |
| Allure Report | Allure + GitHub Pages | `gh-pages` branch |
| Coverage | Codecov | codecov.io badge |
| CI Status | GitHub Actions | Workflow badges in README |
