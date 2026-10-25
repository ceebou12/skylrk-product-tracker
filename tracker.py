
from bs4 import BeautifulSoup
import requests
from database import save_products
from database import get_status

url = 'https://skylrk.com/'

page = requests.get(url, timeout=10)
page.raise_for_status()

#parses the html
soup = BeautifulSoup(page.text, "html.parser") 


products = []

#find everything with this class
for element in soup.find_all(class_= "floating-product-grid__item"): 
	
	#finds image tag that has src attribute (image link) and stores the result
	imgLink_element = element.find("img", attrs={"src": True})
	imgLink = imgLink_element["src"]

	#find aria-label (item name and status) attribute inside the class and store result
	label_element = element.find(attrs={"aria-label": True}) 
	label = label_element["aria-label"]

	#checks if a element (item link) exists and stores it appropriatly
	link_element = element.find("a")
	if link_element != None:
		link = link_element["href"]
	else:
		link = None

	#seperates the item name and status, appends everything to products
	if link != None and link.startswith("/products/"):
		full_url = "https://skylrk.com" + link

		result = get_status(full_url)

		if result != None:
			products.extend(result)
		
	#finds when link exists and finishes url 
	elif label.startswith("View "):
		name = label.replace("View ", "", 1)
		
		if link != None and link.startswith("/products/"):
			full_url = "https://skylrk.com" + link
		else:
			full_url = None

		if full_url != None:
			result = (get_status(full_url))
			if result != None:
				products.extend(result)
		
save_products(products)





