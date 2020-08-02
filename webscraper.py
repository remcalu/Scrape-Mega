import requests
from bs4 import BeautifulSoup
result = requests.get("https://www.google.com/")
print(result.status_code)