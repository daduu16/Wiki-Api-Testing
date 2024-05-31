import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore
import wikipedia
import requests

def get_wikipedia_api_search_suggestions(query):
    return wikipedia.search(query)

def get_wikipedia_api_page_title(page_title):
    return wikipedia.page(page_title).title

def get_wikipedia_api_geosearch(latitude, longitude):
    return wikipedia.geosearch(latitude, longitude)

def get_wikipedia_api_page_url(page_title):
    return wikipedia.page(page_title).url

def take_screenshot(driver, name):
    driver.save_screenshot(f"{name}.png")

@pytest.fixture(scope="session", params=["chrome", "edge"])
def browser(request):
    return request.param

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

@pytest.mark.parametrize("query", ["Python"])
def test_suggest(driver, query):
    suggestions_api = get_wikipedia_api_search_suggestions(query)
    driver.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&format=json")
    
    xpath = "/html/body/pre"  # Default XPath for Chrome
    
    if driver.capabilities['browserName'] == 'MicrosoftEdge':
        xpath = "/html/body/div[3]/div[2]/div[2]"  # XPath for Edge
    
    try:
        pre_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        suggestions_browser = eval(pre_element.text)[1]
    except:
        take_screenshot(driver, "test_suggest")
        raise

    print(f"Library suggestions: {suggestions_api}")
    print(f"Browser suggestions: {suggestions_browser}")
    overlap = set(suggestions_api).intersection(suggestions_browser)
    overlap_count = len(overlap)
    min_count = min(len(suggestions_api), len(suggestions_browser))
    
    print(Fore.GREEN + f"Overlap: {overlap}, Count: {overlap_count}, Min Count: {min_count}")
    assert overlap_count >= min_count * 0.3, \
        f"Not enough overlap. Library: {wikipedia.search(query)} Browser: {suggestions_browser}"
    print(Fore.GREEN + "PASSED test_suggest")

@pytest.mark.parametrize("page_title", ["Python (programming language)"])
def test_page_title(driver, page_title):
    page_api = get_wikipedia_api_page_title(page_title)
    driver.get(f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={page_title}")

    xpath = "/html/body/pre"  # Default XPath for Chrome
    
    if driver.capabilities['browserName'] == 'MicrosoftEdge':
        xpath = "/html/body/div[3]/div[2]/div[2]"  # XPath for Edge
    
    try:
        pre_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        page_browser = eval(pre_element.text)['query']['pages']
        page_browser_title = list(page_browser.values())[0]['title']
    except:
        take_screenshot(driver, "test_page_title")
        raise
    
    print(f"Library title: {wikipedia.page(page_title).title}")
    print(f"Browser title: {page_browser_title}")
    assert page_browser_title == wikipedia.page(page_title).title, \
        f"Titles do not match. Library: {wikipedia.page(page_title).title}, Browser: {page_browser_title}"
    print(Fore.GREEN + "PASSED test_page_title")

@pytest.mark.parametrize("latitude,longitude", [(37.7749, -122.4194)])
def test_geosearch(driver, latitude, longitude):
    places_api = get_wikipedia_api_geosearch(latitude, longitude)
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord={latitude}|{longitude}&format=json"

    try:
        response = requests.get(url)
        response.raise_for_status() 
        response_json = response.json()
        places_browser = [place['title'] for place in response_json['query']['geosearch']]
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        raise

    print(f"Library places: {places_api}")
    print(f"Browser places: {places_browser}")
    overlap = set(places_api).intersection(places_browser)
    overlap_count = len(overlap)
    min_count = min(len(places_api), len(places_browser))
    
    print(Fore.GREEN + f"Overlap: {overlap}, Count: {overlap_count}, Min Count: {min_count}")
    assert overlap_count >= min_count * 0.3, \
        f"Not enough overlap. Library: {places_api} Browser: {places_browser}"
    print(Fore.GREEN + "PASSED test_geosearch")

@pytest.mark.parametrize("page_title", ["Python (programming language)"])
def test_page_url(driver, page_title):
    page_url_api = get_wikipedia_api_page_url(page_title)
    driver.get(f"https://en.wikipedia.org/w/api.php?action=query&prop=info&inprop=url&titles={page_title}&format=json")

    xpath = "/html/body/pre"  # Default XPath for Chrome
    
    if driver.capabilities['browserName'] == 'MicrosoftEdge':
        xpath = "/html/body/div[3]/div[2]/div[2]"  # XPath for Edge
    
    try:
        pre_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        page_url_browser = eval(pre_element.text)['query']['pages']
        page_url_browser = list(page_url_browser.values())[0]['fullurl']
    except:
        take_screenshot(driver, "test_page_url")
        raise
    
    print(f"Library URL: {wikipedia.page(page_title).url}")
    print(f"Browser URL: {page_url_browser}")
    assert wikipedia.page(page_title).url == page_url_browser, \
        f"URLs do not match. Library: {wikipedia.page(page_title).url}, Browser: {page_url_browser}"
    print(Fore.GREEN + "PASSED test_page_url")

# To run the tests, simply use the following command:
# pytest lahiyə.py
