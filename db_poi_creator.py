import sqlite3
import csv
import math

conn = sqlite3.connect("travel_planner.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS poi")
cur.execute("""
CREATE TABLE "poi"(
    "poi_name" TEXT,
    "latitude" REAL,
    "longitude" REAL,
    "num_links" INTEGER,
    "links" TEXT,
    "num_categories" INTEGER,
    "categories" TEXT
)
""")

file_name = input("Enter the imported csv file name: ")
if len(file_name) < 1:
    file_name = "poi_pipe.csv"

with open(file_name, encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter="|")
    lead = True
    for row in csv_reader:
        if lead:
            lead = False
            continue
        # print(row)
        poi_name = row[0]
        latitude = float(row[1]) * 180 / math.pi
        longitude = float(row[2]) * 180 / math.pi
        num_links = row[3]
        links = row[4]
        num_categories = row[5]
        categories = row[6]

        cur.execute("""INSERT INTO poi(poi_name, latitude, longitude, num_links, links, num_categories, 
        categories) VALUES (?, ?, ?, ?, ?, ?, ?)""", (poi_name, latitude, longitude, num_links, links, num_categories,
                                                      categories))
        conn.commit()
