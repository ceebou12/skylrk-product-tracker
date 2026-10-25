from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime

def get_status(url):
	#puts js in url to go through json file
	if "?" in url and ".js" not in url:
		indx = url.index("?")
		result = url[:indx] + ".js" + url[indx:]
	elif "?" not in url and ".js" not in url:
		result = url + ".js"
	
	else:
		result = url
	try:
		response = requests.get(result, timeout=10)
		response.raise_for_status()
		data = response.json()
	except requests.RequestException as e:
		print("Could not check product:", url)
		print(e)
		return None


	all_data = []

	status_result = ""
	full_name = ""
	for variant in data["variants"]:
		full_link = "https://skylrk.com/products/" + str(data["handle"]) + "?variant=" + str(variant["id"])
		if variant["option2"] != None:
			full_name = str(data["title"]) + " " + str(variant["option1"]) + " " + str(variant["option2"])
		else:
			full_name = str(data["title"]) + " " + str(variant["option1"])
		if variant["available"] == True:
			status_result = "Listed"
		else:
			status_result = "Sold out"

		if variant["featured_image"] is not None:
			imgLink = variant["featured_image"]["src"]
		else:
			imgLink = None	

		all_data.append([str(full_name), str(status_result), str(full_link), imgLink])
	
	return all_data

def days_since(date_str):
	today = datetime.date.today()
	date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
	result = (today - date_obj).days
	return result


def save_products(products):
	connection = sqlite3.connect("skylrk.db")

	connection.execute(
		'CREATE TABLE IF NOT EXISTS products (Id INTEGER PRIMARY KEY, Name TEXT, status TEXT, url TEXT UNIQUE, imgLink TEXT, existing INTEGER, last_seen TEXT, days_gone INTEGER)'
	)

	connection.execute('UPDATE products SET existing = 0')
	today = str(datetime.date.today())
	
	for name, status, link, imgLink in products:
		if link != None: 
			connection.execute(
				'''
				INSERT INTO products (Name, status, url, imgLink, existing, last_seen, days_gone) 
				VALUES (?, ?, ?, ?, 1, ?, 0)
				ON CONFLICT(url) DO UPDATE SET 
					Name = excluded.Name,
					status = excluded.status,
					imgLink = excluded.imgLink,
					existing = 1,
					last_seen = excluded.last_seen,
					days_gone = 0
					
				''',
				(name, status, link, imgLink, today) 
			)
			
		else:
			if imgLink is not None:
				result = connection.execute(
							"SELECT imgLink FROM products WHERE imgLink = ?", 
							(imgLink,)
							)
				existing_product = result.fetchone() 

				if existing_product is None: 
					connection.execute("INSERT INTO products (Name, status, url, imgLink, existing, last_seen, days_gone) VALUES (?, ?, ?, ?, 1, ?, 0)", (name, status, link, imgLink, today))
					
				else:
					connection.execute("UPDATE products SET existing = 1, last_seen = ?, days_gone = 0 WHERE imgLink = ?", (today, imgLink,))
	
	not_seen_result = connection.execute('SELECT last_seen, imgLink FROM products WHERE existing = 0')
	not_seen = not_seen_result.fetchall()

	if not_seen:
		for i in range(len(not_seen)):
			days_result = days_since(not_seen[i][0])
			connection.execute('UPDATE products SET days_gone = ? WHERE imgLink = ?',(days_result, not_seen[i][1]))

	DESC_daysgone = connection.execute('SELECT * FROM products ORDER BY days_gone DESC')
	
	


	result = connection.execute(
		'SELECT Name, status, url, imgLink, existing FROM products'
	)

	name_days = connection.execute('SELECT Name, days_gone FROM products WHERE days_gone > 0 ORDER BY days_gone DESC')
	for name, days in name_days:
		pass
	

	connection.execute('''CREATE TABLE IF NOT EXISTS product_history
		(id INTEGER PRIMARY KEY, 
			product_id INTEGER, 
			event TEXT, 
			date TEXT,
			UNIQUE(product_id, event, date))''')

	
	nonexisting = connection.execute('SELECT url FROM products WHERE existing = 0 AND url IS NOT NULL')
	for row in nonexisting:
		url = row[0]
		
		if url is not None:
			stock_status = None 
			if stock_status is None:
				continue
			if stock_status is False:
				status = "Sold out"
				
			else:
				status = "Listed"
			
			connection.execute('UPDATE products SET status = ? WHERE url = ?',
				(status, url,))


	connection.commit()
	connection.close()
