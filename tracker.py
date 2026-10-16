
from bs4 import BeautifulSoup
import requests
#-------function to compare and remove duplicates
def remove_duplicates(products):
	midpoint = len(products) // 2 #lists everything twice, find midway point

	first_half = products[:midpoint]
	second_half = products[midpoint:]



	if first_half == second_half: # Check whether the halves are identical
	    print("The two halves match!")
	    return first_half
	else:
	    print("The two halves do not match!")
	    print("First half:", first_half)
	    print("Second half:", second_half)
	    return products
#-------------------------

url = 'https://skylrk.com/'

page = requests.get(url, timeout=10)
page.raise_for_status()

soup = BeautifulSoup(page.text, "html.parser") # parses the html

products = []
'''

for element in soup.find_all(attrs={"aria-label": True}): # find elements with aria-label
    label = element["aria-label"]

    if "Sold out" in label:
        name = label.replace(" — Sold out", "")
        products.append([name, "Sold out"]) 
        

    elif label.startswith("View "):
        name = label.replace("View ", "", 1)

        products.append([name, "Listed"])
        
products = remove_duplicates(products)

for name, status in products:
    print(name, "-", status)




prod_URL = []

for element in soup.find_all("a", href=True): # find elements with a attr
    link = element["href"]
    if link.startswith("/products/"):
    	full_url = "https://skylrk.com" + link
    	prod_URL.append(full_url)

prod_URL = remove_duplicates(prod_URL)

for link in prod_URL:
	print(link)

'''
products = []

for element in soup.find_all(class_= "floating-product-grid__item"):
	label_element = element.find(attrs={"aria-label": True})
	label = label_element["aria-label"]
	link_element = element.find("a")
	if link_element != None:
		link = link_element["href"]
	else:
		link = None


	if "Sold out" in label:
		name = label.replace(" — Sold out", "")
		products.append([name, "Sold out", link]) 





	elif label.startswith("View "):
		name = label.replace("View ", "", 1)
		
		if link != None and link.startswith("/products/"):
			full_url = "https://skylrk.com" + link
		else:
			full_url = None


		products.append([name, "Listed", full_url])
	
for name, status, link in products:
	print(name, "-", status, "-", link)





