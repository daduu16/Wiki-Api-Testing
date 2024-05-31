import requests

def get_page_id(title):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "info",
        "inprop": "url",
        "format": "json",
        "titles": title
    }

    response = requests.get(url, params=params)
    data = response.json()

    page_id = next(iter(data['query']['pages'].values()))['pageid']
    return page_id

title = "Python (programming language)"
page_id = get_page_id(title)
print(f"The ID of the page '{title}' is {page_id}")