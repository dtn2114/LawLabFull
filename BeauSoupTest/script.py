#import csv
import MySQLdb
from collections import defaultdict
import json
import datetime

"""
This script creates at table in the entities database that records, for each entry in
the non_derivatives3 database, whether it is an AMOUNT of stock shares or a DOLLAR AMOUNT
of debt securities.

"""

def get_owner_type(owner_list):

    """
    if both 'director' and 'officer' are checked, consider the owner an 'officer
    officer returns 0, director returns 1, 10% owner returns 2, none returns 3
    '"""
    if owner_list[1] == 1:
        return 0
    elif owner_list[0] == 1:
        return 1
    elif owner_list[2] == 1:
        return 2
    else:
        return 3

if __name__ == '__main__':

    db = MySQLdb.connect("localhost", "root", "Edgar20!4", "def14a")
    cursor = db.cursor()

    sql = '''CREATE TABLE IF NOT EXISTS securities_test(
                        id MEDIUMINT NOT NULL AUTO_INCREMENT,
                        filer_cik INT(11) NOT NULL,
                        filing_date DATE,
                        issuer_cik INT(11),
                        title VARCHAR(255),
                        title_foot TEXT,
                        shares_owned DECIMAL(15,4),
                        shares_owned_foot TEXT,
                        d_vs_e CHAR(1),
                        PRIMARY KEY(id)
              )'''
    cursor.execute(sql)

    db.close()
    print "Securities Test DB created"

    query = "INSERT INTO securities_test(`filer_cik`, `filing_date`, `issuer_cik`, `title`, `title_foot`, `shares_owned`, `shares_owned_foot`, `d_vs_e`)"\
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"

    db = MySQLdb.connect("localhost", "root", "Edgar20!4", "entities")
    cursor = db.cursor()

    cursor.execute("select filer_cik, filing_date, issuer_cik, title, title_foot, shares_owned, shares_owned_foot from non_derivative3")
    data = cursor.fetchall()

    for d in data:

        insert_list = list(d[0:3])


        title = d[3]
        title_foot = d[4]
        shares = d[5]
        shares_foot = d[6]

        if title:
            if 'stock' in title.lower() or 'share' in title.lower():
                d_vs_e = 'E'
            else:
                d_vs_e = 'D'
        else:
            d_vs_e = None

        insert_list.extend([title, title_foot, shares, shares_foot, d_vs_e])

        try:
            cursor.execute(query, tuple(insert_list))
            db.commit()
            print "db_updated"
        except MySQLdb.Error as e:
            db.rollback()
            print e

    db.close()

    print "done"


