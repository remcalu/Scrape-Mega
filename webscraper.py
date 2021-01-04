# Generate EXE with pyinstaller --onefile webscraper.py --hidden-import jinja2 --add-data C:\Users\RemCa\AppData\Local\Programs\Python\Python38-32\Lib\site-packages\pandas\io\formats\templates\html.tpl;pandas\io\formats\templates
import requests
import pandas as pd
import datetime
import re
from bs4 import BeautifulSoup

##### Set price ranges here #####
minimum = "500"
maximum = "10000"
##### Set price ranges here #####

# Functions
def highlight_savings(val):
    if not re.search('[a-zA-Z]', str(val)):
        if float(val) != 0:
            return 'background-color: #d09950'

def highlight_RAM(val):
    if not 'Unknown' in str(val):
        return 'background-color: #ff33ff'

def highlight_GPU(val):
    if 'GTX' in val or 'RTX' in val:
        return 'background-color: #92D050'
    if 'Radeon' in val:
        return 'background-color: #d05050'

def highlight_CPU(val):
    if 'Intel' in val:
        return 'background-color: #5074d0'
    if 'AMD' in val:
        return 'background-color: #d05050'

def make_clickable(val):
    return '<a target="_blank" href="{}">Link</a>'.format(val, val)

# Various computer specs
gpu_list = ["1050ti", "1050", "1060ti", "1060", "1070ti", "1070", "1650ti", "1650", "1660ti", "1660", "2050ti", "2050", "2060ti", "2060", "2070ti", "2070", "2080ti", "2080super", "2080", "5500m", "1080"]
fancy_gpu_list = ["GTX 1050Ti", "GTX 1050", "GTX 1060Ti", "GTX 1060", "GTX 1070Ti", "GTX 1070", "GTX 1650Ti", "GTX 1650", "GTX 1660Ti", "GTX 1660", "RTX 2050Ti", "RTX 2050", "RTX 2060Ti", "RTX 2060", "RTX 2070Ti", "RTX 2070", "RTX 2080Ti", "RTX 2080 Super", "RTX 2080", "Radeon RX5500M", "GTX 1080"]
ram_list = ["64gb", "64g", "32gb", "32g", "16gb", "16g", "8gb", "8g", "12gb", "12g"]
fancy_ram_list = ["64", "64", "32", "32", "16", "16", "8", "8", "12", "12"]
cpu_list = ["3750h", "4600h", "4800h", "4900hs", "7700hq", "8300h", "8550u", "8750h", "9300h", "9750h", "10300h", "10750h", "10875h", "10980hk", "1065g7", "1185g7"]
fancy_cpu_list = ["AMD R7 3750H", "AMD R5 4600H", "AMD R7 4800H", "AMD R9 4900HS", "Intel i7-7700HQ", "Intel i5-8300H","Intel i7-8550U", "Intel i7-8750H", "Intel i5-9300H", "Intel i7-9750H", "Intel i5-10300H", "Intel i7-10750H", "Intel i7-10875H", "Intel i9-10980HK", "Intel i7-1065G7", "Intel i7-1185G7"]

# Main loop that lasts forever and repeats every 20 minutes
try:
    product_list_link = []
    product_list_name = []
    product_list_price = []
    product_list_saving = []
    product_list_name_cpu = []
    product_list_name_gpu = []
    product_list_name_ram = []

    product_amount = 0
    found = 0
    total_sales = 0

    # Getting data from Canada Computers
    for i in range(2):
        check_if_products = 0
        print("reach1")
        site_string_template = "https://www.canadacomputers.com/search/results_details.php?language=en&keywords=gaming%20laptop&isort=price&pr=%2524"+minimum+"%2B-%2B%2524"+maximum+"&"
        site_string_page = site_string_template + "&page_num=" + str(i)
    
        result = requests.get(site_string_page)
        source = result.content
        soup = BeautifulSoup(source, 'lxml')
        products = soup.find_all('a', 'text-dark text-truncate_3')
        for product in products:
            link = product.attrs['href']
            product_list_link.append(link)

            product_result = requests.get(link)
            product_source = product_result.content
            product_soup = BeautifulSoup(product_source, 'lxml')

            descriptions = product_soup.find_all('h1')
            for description in descriptions:
                if "gaming" in description.text.lower() or "laptop" in description.text.lower() or "notebook" in description.text.lower():
                    #print(description.text)
                    product_list_name.append(description.text)

            prices = product_soup.find_all('strong')
            for price in prices:
                if "$" in price.text:
                    price = price.text[1:].replace(",", "")
                    product_list_price.append(price)

            savings = product_soup.find_all('div', 'pi-price-discount')
            for saving in savings:
                if "$" in saving.text:
                    saving_value = saving.text[8:].split('\n')
                    discount = saving_value[1]
                    discount = discount[1:].replace(",", "")
                    product_list_saving.append(discount)
                    total_sales+=1
            if not savings:
                product_list_saving.append("0.00")

            product_amount+=1
            check_if_products = 1
            print("Scanned:",product_amount,"products")

        if check_if_products == 0:
            break

    # Cleaning up the data that will be pushed to the spreadsheet
    product_list_name_copy = product_list_name.copy()
    for i in range(product_amount):
        product_list_name_copy[i] = product_list_name_copy[i].replace(" ", "")
        
        # For RAM
        for j in range(len(ram_list)):
            if ram_list[j] in product_list_name_copy[i].lower():
                product_list_name_ram.append(fancy_ram_list[j])
                found = 1
                break
        if found == 0:
            product_list_name_ram.append("Unknown")
        found = 0
        
        # For GPUs
        for j in range(len(gpu_list)):
            if gpu_list[j] in product_list_name_copy[i].lower():
                product_list_name_gpu.append(fancy_gpu_list[j])
                found = 1
                break
        if found == 0:
            product_list_name_gpu.append("Unknown")
        found = 0
        
        # For CPUs
        for j in range(len(cpu_list)):
            if cpu_list[j] in product_list_name_copy[i].lower():
                product_list_name_cpu.append(fancy_cpu_list[j])
                found = 1
                break
        if found == 0:
            product_list_name_cpu.append("Unknown")
        found = 0

    # Create data frame
    data = pd.DataFrame({'Links': product_list_link, 'Descriptions': product_list_name, 'Prices': product_list_price, 'Savings': product_list_saving, 'RAM': product_list_name_ram, 'GPU': product_list_name_gpu, 'CPU': product_list_name_cpu})
    data.style.set_properties(**{'text-align': 'left'})
    for i in range(len(data['RAM'])):
        if (data['RAM'][i] != 'Unknown'):
            data['RAM'][i] = int(data['RAM'][i])

    data["Prices"] = data["Prices"].astype(float)
    data["Savings"] = data["Savings"].astype(float)

    # Write to excel
    print("reach2")
    currdatetime = str(datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")) 
    writer = pd.ExcelWriter("saved/datasheet(" + currdatetime + ").xlsx",engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Report')

    workbook = writer.book
    worksheet = writer.sheets['Report']
    money_fmt = workbook.add_format({'num_format': '$#,##0', 'align': 'left'})
    ram_fmt = workbook.add_format({'align': 'left'})

    worksheet.set_column('B:B', 5)
    worksheet.set_column('C:C', 100)
    worksheet.set_column('D:D', 8, money_fmt)
    worksheet.set_column('E:E', 8, money_fmt)
    worksheet.set_column('F:F', 8, ram_fmt)
    worksheet.set_column('G:G', 17)
    worksheet.set_column('H:H', 15)

    # Set colors
    green_fmt = workbook.add_format({'bg_color':'#92D050'})
    red_fmt = workbook.add_format({'bg_color':'#d05050'})
    blue_fmt = workbook.add_format({'bg_color':'#5074d0'})
    orange_fmt = workbook.add_format({'bg_color':'#d09950'})
    grey_fmt = workbook.add_format({'bg_color':'#c7c7c7'})
    purple_fmt = workbook.add_format({'bg_color':'#ff33ff'})

    worksheet.conditional_format('G2:G'+str(product_amount+1), {'type':'text', 'criteria':'containing', 'value':'GTX', 'format':green_fmt})
    worksheet.conditional_format('G2:G'+str(product_amount+1), {'type':'text', 'criteria':'containing', 'value':'RTX', 'format':green_fmt})
    worksheet.conditional_format('G2:G'+str(product_amount+1), {'type':'text', 'criteria':'containing', 'value':'Radeon', 'format':red_fmt})
    worksheet.conditional_format('H2:H'+str(product_amount+1), {'type':'text', 'criteria':'containing', 'value':'Intel', 'format':blue_fmt})
    worksheet.conditional_format('H2:H'+str(product_amount+1), {'type':'text', 'criteria':'containing', 'value':'AMD', 'format':red_fmt})
    worksheet.conditional_format('E2:E'+str(product_amount+1), {'type':'text', 'criteria':'begins with', 'value':'0', 'format':grey_fmt})
    worksheet.conditional_format('E2:E'+str(product_amount+1), {'type':'text', 'criteria':'containing', 'value':'', 'format':orange_fmt})
    for i in range(len(data['RAM'])):
        if (data['RAM'][i] != 'Unknown'):
            int(data['RAM'][i])
            worksheet.conditional_format('F'+str(2+i), {'type':'text', 'criteria':'containing', 'value':'', 'format':purple_fmt})
    #worksheet.conditional_format('F2:F'+str(product_amount+1), {'type':'2_color_scale', 'min_color':'#c98dc9', 'max_color':'#d050d0'})
    worksheet.conditional_format('B2:H'+str(product_amount+1), {'type':'text', 'criteria':'containing', 'value':'', 'format':grey_fmt})
    
    writer.save()
    print("Created excel file at", currdatetime, "!")

    df = pd.read_excel("saved/datasheet(" + currdatetime + ").xlsx", engine='openpyxl')
    df = df.drop(columns="Unnamed: 0")

    df["Prices"] = df["Prices"].astype(float).map('{:.2f}'.format)
    df["Savings"] = df["Savings"].astype(float).map('{:.2f}'.format)

    df.to_html("public/data.html")
    s = df.style.applymap(highlight_savings, subset = pd.IndexSlice[:, ['Savings']])
    s = s.applymap(highlight_RAM, subset = pd.IndexSlice[:, ['RAM']])
    s = s.applymap(highlight_GPU, subset = pd.IndexSlice[:, ['GPU']])
    s = s.applymap(highlight_CPU, subset = pd.IndexSlice[:, ['CPU']])
    s = s.format({'Links': make_clickable})
    myhtml = df.style.set_properties().render()

    # Optional html prettify
    #myhtml = BeautifulSoup(myhtml)
    #myhtml = myhtml.prettify()

    # Writing non styled file
    with open('public/data.html', 'w') as contents:
        contents.write(myhtml)     

    # Writing some style to the file
    with open('public/data.html', 'w') as contents:
        contents.write(s.render())

    # Writing a link to css sheet
    with open('public/data.html', 'r') as contents:
        save = contents.read()
    with open('public/data.html', 'w') as contents:
        contents.write("<link rel=\"stylesheet\" href=\"style.css\">\n")
    with open('public/data.html', 'a') as contents:
        contents.write(save)

    print("# of products scraped with BS4:", product_list_name)
    print("Done!")
except Exception as e:
    print("Exception", e, "caught")
    print("Attempting to loop again in 20 minutes!")
