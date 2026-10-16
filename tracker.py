
from bs4 import BeautifulSoup
import requests

url = 'https://skylrk.com/'

page = requests.get(url, timeout=10)
page.raise_for_status()

soup = BeautifulSoup(page.text, "html.parser") # parses the html

products = []

for element in soup.find_all(attrs={"aria-label": True}): # find elements with aria-label
    label = element["aria-label"]

    if "Sold out" in label:
        name = label.replace(" — Sold out", "")
        products.append([name, "Sold out"]) 
        

    elif label.startswith("View "):
        name = label.replace("View ", "", 1)

        products.append([name, "Listed"])

midpoint = len(products) // 2 #lists everything twice, find midway point

first_half = products[:midpoint]
second_half = products[midpoint:]



if first_half == second_half: # Check whether the halves are identical
    print("The two halves match!")
    products = first_half
else:
    print("The two halves do not match!")
    print("First half:", first_half)
    print("Second half:", second_half)

for name, status in products:
    print(name, "-", status)

'''

'''
