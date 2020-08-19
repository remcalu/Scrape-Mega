# CanadaComputers site Webscraper

## Author
Remus Calugarescu

## Last Modified
August 18, 2020

## Purpose
This is a webscraper that looks for gaming laptop on the CanadaComputers website (http://canadacomputers.com/). After scraping the data, a spreadsheet is updated with current prices, sales, specificaitons such as RAM, CPU and GPU of each laptop. If there's a different amount of deals or sales compared to the last time the data was scraped, where the data is stored in text files, an email is sent to an email address users choice that notifies the user that the amount of deals or sales has changes. The program persists indefinitely and repeats every 20 minutes

![Options](https://i.imgur.com/RIVldIy.png)

## Instructions
To be able to run the script you must have Python and Pip installed, then you must Pip installs
~~~~
$ pip install requests
~~~~
`<$ pip install pandas>`
`<$ pip install bs4>`
`<$ pip install lxml>`
`<$ pip install xlsxwriter>`
`<$ pip install jinja2>`

## Notes
- You MUST enter a valid email address near the bottom of the program for it to execute
