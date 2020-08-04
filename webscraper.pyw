#https://www.canadacomputers.com/search/results_details.php?language=en&keywords=gaming+laptop&page_num=2
import requests
import pandas as pd
import smtplib 
import time
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
from bs4 import BeautifulSoup

# Getting data from CanadaComputers, checking for computers between $800 and $1500
while(True):
    productListLink = []
    productListName = []
    productListPrice = []
    productListSaving = []
    productListNameCPU = []
    productListNameGPU = []
    productListNameRAM = []
    productAmount = 0
    foundCPU = 0
    totalSales = 0

    # Site specific portion
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
                                productListSaving.append(savingValue[1])
                                totalSales+=1
                        if not savings:
                            productListSaving.append("$0.00")

                        productAmount+=1
                        print("Scanned:",productAmount,"products")
            except:
                pass

    # Non site specific portion
    print("Product Amount: [",productAmount,"]")

    # Checking if new laptop added
    f = open("laptopAmount.txt", "r")
    f2 = open("salesAmount.txt", "r")
    oldTotalLaptops = f.read()
    oldTotalLaptopSales = f2.read()
    f = open("laptopAmount.txt", "w")
    f2 = open("salesAmount.txt", "w")
    f.write(str(productAmount)+" ")
    totalLaptops = (str(productAmount)+" ")
    f2.write(str(totalSales)+" ")
    totalLaptopSales = (str(totalSales)+" ")
    f.close()
    f2.close

    for i in range(productAmount):
        # For RAM
        if "8gb" in productListName[i].lower() or "8 gb" in productListName[i].lower() or "8g" in productListName[i].lower() or "8 g" in productListName[i].lower():
            productListNameRAM.append("8gb")
        elif "12gb" in productListName[i].lower() or "12 gb" in productListName[i].lower() or "12g" in productListName[i].lower() or "12 g" in productListName[i].lower():
            productListNameRAM.append("12gb")
        elif "16gb" in productListName[i].lower() or "16 gb" in productListName[i].lower() or "16g" in productListName[i].lower() or "16 g" in productListName[i].lower():
            productListNameRAM.append("16gb")
        elif "32gb" in productListName[i].lower() or "32 gb" in productListName[i].lower() or "32g" in productListName[i].lower() or "32 g" in productListName[i].lower():
            productListNameRAM.append("32gb")
        else:
            productListNameRAM.append("Unknown")
        
        # For GPUs (Only gpu's that I'd be intrested in)
        if "1050" in productListName[i]:
            productListNameGPU.append("GTX 1050")
        elif "1050TI" in productListName[i].upper():
            productListNameGPU.append("GTX 1050TI")
        elif "1060" in productListName[i]:
            productListNameGPU.append("GTX 1060")
        elif "1060TI" in productListName[i].upper():
            productListNameGPU.append("GTX 1060TI")
        elif "1650" in productListName[i]:
            productListNameGPU.append("GTX 1650")
        elif "1650TI" in productListName[i].upper():
            productListNameGPU.append("GTX 1650TI")
        elif "1660" in productListName[i]:
            productListNameGPU.append("GTX 1660")
        elif "1660TI" in productListName[i].upper():
            productListNameGPU.append("GTX 1660TI")
        elif "2050" in productListName[i]:
            productListNameGPU.append("GTX 2050")
        elif "2050TI" in productListName[i].upper():
            productListNameGPU.append("GTX 2050TI")
        elif "2060" in productListName[i]:
            productListNameGPU.append("GTX 2060")
        elif "2060TI" in productListName[i].upper():
            productListNameGPU.append("GTX 2060TI")
        elif "2070" in productListName[i]:
            productListNameGPU.append("GTX 2070")
        elif "2070TI" in productListName[i].upper():
            productListNameGPU.append("GTX 2070TI")
        else:
            productListNameGPU.append("Unknown")

        # For CPUs
        for j in range(len(productListName[i])):
            if productListName[i][j].upper() == "H" and j != 0 and productListName[i][j-1].isdigit() == True and (productListName[i][j+1] == ' ' or productListName[i][j+1] == ','):
                cpuID = ""
                for k in range(1000):
                    if productListName[i][j-k] == '-' or productListName[i][j-k] == ' ':
                        break
                    cpuID += productListName[i][j-k]
                cpuID = cpuID[::-1]
                cpuNumber = cpuID[:-1]
                if int(cpuNumber) > 6000:
                    productListNameCPU.append("Intel "+cpuID)
                else:
                    productListNameCPU.append("AMD "+cpuID)
                foundCPU = 1
            if len(productListName[i])-1 == j:
                productListNameCPU.append("Unknown")
                foundCPU = 1
            if foundCPU == 1:
                foundCPU = 0
                break

    # Create data frame
    data = pd.DataFrame({'Links': productListLink, 'Descriptions': productListName, 'Prices': productListPrice, 'Savings': productListSaving, 'RAM': productListNameRAM, 'GPU': productListNameGPU, 'CPU': productListNameCPU})

    # Write to excel
    writer = pd.ExcelWriter("FromPython.xlsx",engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Report')

    workbook = writer.book
    worksheet = writer.sheets['Report']

    money_fmt = workbook.add_format({'num_format': '$#,##0', 'bold': True})

    worksheet.set_column('B:B', 5)
    worksheet.set_column('C:C', 150)
    worksheet.set_column('H:H', 12)

    writer.save()

    # Email stuff
    if totalLaptops != oldTotalLaptops or totalLaptopSales != oldTotalLaptopSales:
        # creates SMTP session 
        email = smtplib.SMTP('smtp.gmail.com', 587) 

        # TLS for security 
        email.starttls() 

        # authentication
        # compiler gives an error for wrong credential. 
        email.login("", "") 

        # message to be sent
        message = '''\
From: Python Script
Subject: *Laptop Search Update*
%s Laptops
%s On sale
        ''' % (totalLaptops, totalLaptopSales)

        # sending the mail 
        email.sendmail("", "", message) 

        # terminating the session 
        email.quit()
    time.sleep(1200)