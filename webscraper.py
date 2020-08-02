#https://www.canadacomputers.com/search/results_details.php?language=en&keywords=gaming+laptop&page_num=2
import requests
from bs4 import BeautifulSoup

productListName = []
productListPrice = []
productAmount = 0

for i in range(10):
    siteStringTemplate = "https://www.canadacomputers.com/search/results_details.php?language=en&keywords=gaming%20laptop&isort=price&pr=%2524800%2B-%2B%25241500&"
    siteStringPage = siteStringTemplate + "&page_num=" + str(i)
    result = requests.get(siteStringPage)

    source = result.content
    soup = BeautifulSoup(source, 'lxml')
    
    products = soup.findAll('span')

    for product in products:
        aTag = product.find('a')
        try:
            if 'href' in aTag.attrs:
                link = aTag.get('href')
                if "canadacomputers" in link:
                    print("\n")
                    print(link)
                    print(product.text)
                    productAmount+=1
        except:
            pass
print("Product Amount: [",productAmount,"]")

