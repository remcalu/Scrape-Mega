#https://www.canadacomputers.com/search/results_details.php?language=en&keywords=gaming+laptop&page_num=2
import requests
from bs4 import BeautifulSoup

# Getting data from CanadaComputers, checking for computers between $800 and $1500
productListLink = []
productListName = []
productListPrice = []
productListSaving = []
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
            if "href" in aTag.attrs:
                link = aTag.get('href')
                if "canadacomputers" in link:
                    
                    #print("\n")
                    #print(link)
                    productListLink.append(link)

                    productResult = requests.get(link)
                    productSource = productResult.content
                    productSoup = BeautifulSoup(productSource, 'lxml')

                    descriptions = productSoup.findAll('h1')
                    for description in descriptions:
                        if "gaming" in description.text.lower():
                            #print(description.text)
                            productListName.append(description.text)
                        elif "notebook" in description.text.lower():
                            #print(description.text)
                            productListName.append(description.text)
                        elif "laptop" in description.text.lower():
                            #print(description.text)
                            productListName.append(description.text)

                    prices = productSoup.findAll('strong')
                    for price in prices:
                        if "$" in price.text:
                            #print(price.text)
                            productListPrice.append(price.text)

                    savings = productSoup.findAll('div', {"class": "pi-price-discount"})
                    for saving in savings:
                        if "$" in saving.text:
                            savingValue = saving.text[8:]
                            savingValue = savingValue.split('\n')
                            #print(savingValue[1])
                            productListSaving.append(savingValue[0])
                    if not savings:
                        productListSaving.append("$0.00")

                    productAmount+=1
                    print("Scanned:",productAmount,"products")
        except:
            pass

print("Product Amount: [",productAmount,"]")

#print(len(productListLink))
#print(len(productListName))
#print(len(productListPrice))
#print(len(productListSaving))

for i in range(productAmount):
    print("\n")
    print(productListLink[i])
    print(productListName[i])
    print(productListPrice[i])
    print(productListSaving[i])
