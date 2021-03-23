import sqlite3

conn = sqlite3.connect('locations.db')

c = conn.cursor()

c.execute('DROP TABLE IF EXISTS locations')
c.execute('''
	CREATE TABLE "locations" (
		"court_id" TEXT,
		"name" TEXT,
		"tennis_court_area" TEXT,
		"park_name" TEXT,
		"address" TEXT,
		"district" TEXT,
		"ward" TEXT,
		"primary_permitting_status" TEXT,
		"asset_category" TEXT,
		"lights" TEXT,
		"surface_material" TEXT,
		"GIS_coordinate" TEXT
	)
''')

conn.commit()

conn.close()

print('Created locations table')