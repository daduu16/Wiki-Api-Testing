import wikipedia

search_results = wikipedia.search("Python")
print("Search results for 'Python':")
for result in search_results:
    print(result)

page = wikipedia.page("Python (programming language)")

print(f"Title: {page.title}")
print(f"URL: {page.url}")
print(f"Summary: {page.summary}")

suggestions = wikipedia.search("pyth", results=5)
print("Suggestions for 'pyth':")
for suggestion in suggestions:
    print(suggestion)

geosearch_results = wikipedia.geosearch(40.712776, -74.005974)
print("Geosearch results:")
for result in geosearch_results:
    print(result)