# Best Practices — QA Automation Framework

## 1. Test Writing

### ✅ DO

- **One assertion per concept** — multiple `assert` are fine if they test the same behavior
- **Descriptive test names** — `test_locked_user_shows_error` > `test_login_2`
- **Arrange-Act-Assert (AAA)** — always structure tests with clear sections
- **Use `allure.step()`** for multi-step tests — makes reports readable
- **Use `allure.severity`** — mark tests as BLOCKER/CRITICAL/NORMAL/MINOR
- **Use markers** — `@pytest.mark.smoke`, `@pytest.mark.regression`
- **Keep tests independent** — no test should depend on another test's state
- **Use fixtures for setup** — never put navigation in test bodies directly

### ❌ DON'T

- Don't use `time.sleep()` — use explicit waits or `wait_for_*` methods
- Don't hardcode URLs in test files — use `settings` config
- Don't hardcode credentials — use `settings` or JSON fixtures
- Don't put locators in test files — they belong in Page Objects
- Don't ignore flaky tests — fix them or mark them and open an issue
- Don't use `assert` on raw `driver.find_element()` — it throws, doesn't assert

---

## 2. Page Objects

```python
# ✅ GOOD — clean, readable, single responsibility
class LoginPage(BasePage):
    _USERNAME = (By.ID, "user-name")  # private locator
    
    def login(self, username, password):  # public action
        self.type_text(self._USERNAME, username)
        ...

# ❌ BAD — test logic mixed with page interactions
def test_login(driver):
    driver.find_element(By.ID, "user-name").send_keys("user")
    driver.find_element(By.ID, "login-button").click()
    assert "inventory" in driver.current_url  # test knows about locators
```

---

## 3. Waits

```python
# ✅ GOOD — explicit waits via BasePage methods
element = self.find_clickable_element(self._LOGIN_BTN)

# ✅ GOOD — Playwright auto-waits (no wait needed)
page.click("[data-test='login-button']")

# ❌ BAD — never do this
import time
time.sleep(3)
driver.find_element(By.ID, "login-button").click()
```

---

## 4. Test Data

```python
# ✅ GOOD — external fixture
FIXTURES = json.loads(Path("fixtures/users.json").read_text())
user = FIXTURES["valid_users"]["standard"]

# ✅ GOOD — Faker for unique data
from faker import Faker
fake = Faker()
email = fake.email()

# ❌ BAD — hardcoded in test
def test_create_user():
    response = client.post("/users", json={"name": "John", "email": "john@test.com"})
```

---

## 5. CI/CD

- All tests run headless in CI (`HEADLESS=true`)
- Use `--reruns=1` for flaky network-dependent tests
- Always upload artifacts (`--html=reports/*.html`, `--alluredir`)
- Use `if: always()` on upload steps so reports are available even on failure
- Schedule daily regression runs with `cron`

---

## 6. Naming Conventions

| Item | Convention | Example |
|---|---|---|
| Test files | `test_<feature>.py` | `test_login.py` |
| Test classes | `Test<Feature>` | `TestLogin` |
| Test methods | `test_<behavior>` | `test_locked_user_shows_error` |
| Page classes | `<Name>Page` | `LoginPage` |
| Locators | `_SCREAMING_SNAKE` (private) | `_LOGIN_BUTTON` |
| Fixtures | `snake_case` | `authenticated_page` |
| Test IDs | `TC_<SUITE>_<NNN>` | `TC_LOGIN_001` |

---

## 7. Git Workflow

```
main          ← stable, always passing
  │
develop       ← integration branch
  │
feature/TC-001-add-checkout-tests   ← feature branches
bugfix/flaky-login-test             ← bug fix branches
```

**Commit message format:**
```
type(scope): short description

feat(selenium): add checkout E2E tests TC_CHKOUT_004 to TC_CHKOUT_006
fix(api): handle 429 rate limit in api_client retries
docs(readme): update quick start with Playwright instructions
test(playwright): add inventory sorting tests
```
