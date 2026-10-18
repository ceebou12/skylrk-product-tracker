
import sqlite3

def save_products(products):
	connection = sqlite3.connect("skylrk.db")
	connection.execute("DELETE FROM products")

	connection.execute(
		'CREATE TABLE IF NOT EXISTS products (Id INTEGER PRIMARY KEY, Name TEXT, status TEXT, url TEXT UNIQUE, imgLink TEXT)'
	)

	print(connection.execute("PRAGMA table_info(products)").fetchall())

	for name, status, link, imgLink in products:
		if link != None:
			connection.execute(
				'''
				INSERT INTO products (Name, status, url, imgLink)
				VALUES (?, ?, ?, ?)
				ON CONFLICT(url) DO UPDATE SET
					Name = excluded.Name,
					status = excluded.status,
					imgLink = excluded.imgLink
				''',
				(name, status, link, imgLink)
			)
			
		else:
			result = connection.execute(
						"SELECT imgLink FROM products WHERE imgLink = ?",
						(imgLink,)
						)
			existing_product = result.fetchone()


			if existing_product == None and imgLink != None:
				connection.execute("INSERT INTO products (Name, status, url, imgLink) VALUES (?, ?, ?, ?)", (name, status, link, imgLink))
				

	connection.commit()

	result = connection.execute(
		'SELECT Name, status, url, imgLink FROM products'
	)
	print(result.fetchall())

	connection.close()
