import sqlite3
import csv
import datetime
import base64


# Get information for todays date
now = datetime.datetime.now()
# subtract 1 day to get yesterdays date
yesterday = now - datetime.timedelta(days=1)
# make dates into strings
today = now.strftime('%Y-%m-%d')
day = yesterday.strftime('%Y-%m-%d')
filename = f"{day}_OM_PP_entries.csv"

def export():
    """Exports database as csv for given month"""
    with sqlite3.connect("covid_scan.sqlite") as con:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            c = con.cursor()
            for row in c.execute(f"SELECT * from entries WHERE day = ?", (day,)):
                print(row)
                writer.writerow((base64.b64decode(row[0]).decode('utf-8'), *row[1:]))


if __name__ == '__main__':
        export()