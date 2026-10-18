
from bs4 import BeautifulSoup
import requests
from database import save_products

url = 'https://skylrk.com/'

page = requests.get(url, timeout=10)
page.raise_for_status()

soup = BeautifulSoup(page.text, "html.parser") # parses the html


products = []

for element in soup.find_all(class_= "floating-product-grid__item"):
	
	imgLink_element = element.find("img", attrs={"src": True}) #finds image tag that has src attribute
	imgLink = imgLink_element["src"]


	label_element = element.find(attrs={"aria-label": True})
	label = label_element["aria-label"]


	link_element = element.find("a")
	if link_element != None:
		link = link_element["href"]
	else:
		link = None


	if "Sold out" in label:
		name = label.replace(" — Sold out", "")
		products.append([name, "Sold out", link, imgLink]) 


	elif label.startswith("View "):
		name = label.replace("View ", "", 1)
		
		if link != None and link.startswith("/products/"):
			full_url = "https://skylrk.com" + link
		else:
			full_url = None


		products.append([name, "Listed", full_url, imgLink])
		
	
#for name, status, link, imgLink in products:
	#print(name, "-", status, "-", link, "-", imgLink)

save_products(products)





