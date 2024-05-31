import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="browser: chrome or edge"
    )

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def driver(browser):
    from selenium import webdriver
    if browser == "chrome":
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif browser == "edge":
        from selenium.webdriver.edge.service import Service as EdgeService
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    yield driver
    driver.quit()
