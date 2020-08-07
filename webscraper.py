#https://www.canadacomputers.com/search/results_details.php?language=en&keywords=gaming+laptop&page_num=2
import requests
import pandas as pd
import smtplib 
import time
from email import encoders 
from bs4 import BeautifulSoup

# Set price ranges here
minimum = "500"
maximum = "1100"

# Various computer specs
gpuList = ["1050ti", "1050", "1060ti", "1060", "1070ti", "1070", "1080ti", "1080", "1650ti", "1650", "1660ti", "1660", "2050ti", "2050", "2060ti", "2060", "2070ti", "2070", "2080ti", "2080super", "2080", "5500m"]
fancyGpuList = ["GTX 1050Ti", "GTX 1050", "GTX 1060Ti", "GTX 1060", "GTX 1070Ti", "GTX 1070", "GTX 1080Ti", "GTX 1080", "GTX 1650Ti", "GTX 1650", "GTX 1660Ti", "GTX 1660", "RTX 2050Ti", "RTX 2050", "RTX 2060Ti", "RTX 2060", "RTX 2070Ti", "RTX 2070", "RTX 2080Ti", "RTX 2080 Super", "RTX 2080", "Radeon RX5500M"]
ramList = ["64gb", "64g", "32gb", "32g", "16gb", "16g", "8gb", "8g", "12gb", "12g"]
fancyRamList = ["64", "64", "32", "32", "16", "16", "8", "8", "12", "12"]
cpuList = ["3750h", "4600h", "4800h", "4900hs", "7700hq", "8300h", "8550u", "8750h", "9300h", "9750h", "10300h", "10750h", "10875h", "10980hk", "1065g7"]
fancyCpuList = ["AMD R7 3750H", "AMD R5 4600H", "AMD R7 4800H", "AMD R9 4900HS", "Intel i7-7700HQ", "Intel i5-8300H"," Intel i7-8550U", "Intel i7-8750H", "Intel i5-9300H", "Intel i7-9750H", "Intel i5-10300H", "Intel i7-10750H", "Intel i7-10875H", "Intel i9-10980HK", "Intel i7-1065G7"]

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
    found = 0
    totalSales = 0

    # Getting data from Canada Computers
    for i in range(100):
        checkIfProducts = 0

        siteStringTemplate = "https://www.canadacomputers.com/search/results_details.php?language=en&keywords=gaming%20laptop&isort=price&pr=%2524"+minimum+"%2B-%2B%2524"+maximum+"&"
        siteStringPage = siteStringTemplate + "&page_num=" + str(i)
    
        result = requests.get(siteStringPage)
        source = result.content
        soup = BeautifulSoup(source, 'lxml')
        products = soup.findAll('a', 'text-dark text-truncate_3')
        for product in products:
            link = product.attrs['href']
            productListLink.append(link)

            productResult = requests.get(link)
            productSource = productResult.content
            productSoup = BeautifulSoup(productSource, 'lxml')

            descriptions = productSoup.findAll('h1')
            for description in descriptions:
                if "gaming" in description.text.lower() or "laptop" in description.text.lower() or "notebook" in description.text.lower():
                    #print(description.text)
                    productListName.append(description.text)

            prices = productSoup.findAll('strong')
            for price in prices:
                if "$" in price.text:
                    print(price.text[1:])
                    productListPrice.append(price.text[1:].replace(",", ""))

            savings = productSoup.findAll('div', 'pi-price-discount')
            for saving in savings:
                if "$" in saving.text:
                    savingValue = saving.text[8:].split('\n')
                    discount = savingValue[1]
                    print(discount[1:])
                    productListSaving.append(discount[1:].replace(",", ""))
                    totalSales+=1
            if not savings:
                productListSaving.append("0.00")

            productAmount+=1
            checkIfProducts = 1
            print("Scanned:",productAmount,"products\n")

        if checkIfProducts == 0:
            break
           
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
    f2.close()

    productListNameCopy = productListName.copy()
    for i in range(productAmount):
        productListNameCopy[i] = productListNameCopy[i].replace(" ", "")
        # For RAM
        for j in range(len(ramList)):
            if ramList[j] in productListNameCopy[i].lower():
                productListNameRAM.append(fancyRamList[j])
                found = 1
                break
        if found == 0:
            productListNameRAM.append("Unknown")
        found = 0
        
        # For GPUs (Only gpu's that I'd be intrested in)
        for j in range(len(gpuList)):
            if gpuList[j] in productListNameCopy[i].lower():
                productListNameGPU.append(fancyGpuList[j])
                found = 1
                break
        if found == 0:
            productListNameGPU.append("Unknown")
        found = 0
        
        # For CPUs
        for j in range(len(cpuList)):
            if cpuList[j] in productListNameCopy[i].lower():
                productListNameCPU.append(fancyCpuList[j])
                found = 1
                break
        if found == 0:
            productListNameCPU.append("Unknown")
        found = 0

    # Create data frame
    data = pd.DataFrame({'Links': productListLink, 'Descriptions': productListName, 'Prices': productListPrice, 'Savings': productListSaving, 'RAM': productListNameRAM, 'GPU': productListNameGPU, 'CPU': productListNameCPU})
    data.style.set_properties(**{'text-align': 'left'})
    data['RAM'] = data['RAM'].astype(int)
    data['Prices'] = data['Prices'].astype(float)
    data['Savings'] = data['Savings'].astype(float)

    # Write to excel
    writer = pd.ExcelWriter("FromPython.xlsx",engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Report')

    workbook = writer.book
    worksheet = writer.sheets['Report']
    moneyFMT = workbook.add_format({'num_format': '$#,##0', 'align': 'left'})
    ramFMT = workbook.add_format({'align': 'left'})

    worksheet.set_column('B:B', 5)
    worksheet.set_column('C:C', 150)
    worksheet.set_column('D:D', 7, moneyFMT)
    worksheet.set_column('E:E', 7, moneyFMT)
    worksheet.set_column('F:F', 5, ramFMT)
    worksheet.set_column('G:G', 17)
    worksheet.set_column('H:H', 15)

    # Set colors
    greenFMT = workbook.add_format({'bg_color':'#92D050'})
    redFMT = workbook.add_format({'bg_color':'#d05050'})
    blueFMT = workbook.add_format({'bg_color':'#5074d0'})
    orangeFMT = workbook.add_format({'bg_color':'#d09950'})
    greyFMT = workbook.add_format({'bg_color':'#c7c7c7'})

    worksheet.conditional_format('G2:G'+str(productAmount+1), {'type':'text', 'criteria':'containing', 'value':'GTX', 'format':greenFMT})
    worksheet.conditional_format('G2:G'+str(productAmount+1), {'type':'text', 'criteria':'containing', 'value':'RTX', 'format':greenFMT})
    worksheet.conditional_format('G2:G'+str(productAmount+1), {'type':'text', 'criteria':'containing', 'value':'Radeon', 'format':redFMT})
    worksheet.conditional_format('H2:H'+str(productAmount+1), {'type':'text', 'criteria':'containing', 'value':'Intel', 'format':blueFMT})
    worksheet.conditional_format('H2:H'+str(productAmount+1), {'type':'text', 'criteria':'containing', 'value':'AMD', 'format':redFMT})
    worksheet.conditional_format('E2:E'+str(productAmount+1), {'type':'text', 'criteria':'not containing', 'value':'$0.00', 'format':orangeFMT})
    worksheet.conditional_format('F2:F'+str(productAmount+1), {'type':'2_color_scale', 'min_color':'#c98dc9', 'max_color':'#d050d0'})
    worksheet.conditional_format('B2:H'+str(productAmount+1), {'type':'text', 'criteria':'containing', 'value':'', 'format':greyFMT})

    writer.save()
    print("Updated excel file!")

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
        print("Sent email!")
    print("Done! Looping again in 20 minutes!")
    exit()
    time.sleep(1200)