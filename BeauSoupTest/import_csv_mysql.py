#!/usr/bin/python
import csv
import glob
import os
from decimal import *
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import MySQLdb
from collections import defaultdict
import json
import datetime

"""
This script creates at table in the def14a database that records the table from exec_comp into exec test.

"""

if __name__ == '__main__':
    db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "def14a")
    cursor = db.cursor()

    sql = '''CREATE TABLE IF NOT EXISTS bill_exec(
                        id MEDIUMINT NOT NULL AUTO_INCREMENT,
                        name INT(11) NOT NULL,
                        title VARCHAR(255),
                        year INT(11) NOT NULL,
                        salary DEC(32) NOT NULL,
                        bonus DEC(32) NOT NULL,
                        stock awards INT(32) NOT NULL,
                        option awards INT(32) NOT NULL,
                        RSUs INT(10) NOT NULL,
                        non-equity incentive plan compensation INT(11) NOT NULL,
                        change in pension value and non-qualified deferred compensation INT(11) NOT NULL,
                        securities underlying options INT(11) NOT NULL,
                        all other INT(11) NOT NULL,
                        total INT(11) NOT NULL,
                        remainder INT(11) NOT NULL,

              )'''
    cursor.execute(sql)
    db.close()

    print "exec_test2 DB created"
    with open('toMySql.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['TableToMySQL'])

    path = '/Users/bill/PycharmProjects/BeauSoupTest/files/*.htm'
    outpath = '/Users/bill/PycharmProjects/BeauSoupTest/files/'
    for filename in glob.glob(path):
        csvname = os.path.basename(filename)
        csvname = os.path.splitext(csvname)[0]
        filename = ''.join(('file:///', filename))
        csvname = ''.join((outpath, csvname, '.csv'))

        data = csvToArray(csvname)
        table = rearrange_data(data)
        # with open('toMySql.csv', 'ab') as f:
        #     writer = csv.writer(f)
        #     writer.writerow([csvname])
        # writeToCSV(table, 'toMySql.csv', 'ab')
        query = '''INSERT INTO exec_test2 (name, year, title, salary, bonus, stock awards, option awards, RSUs, non-equity ' \
                'incentive plan compensation, change in pension value and non-qualified deferred compensation, ' \
                'all other, total, remainder)' \
                'VALUES("%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s", "%s")'''
        db = MySQLdb.connect("localhost", "root", "Edgar20!4", "def14a")
        cursor = db.cursor()
        for row in table:
            try:
                cursor.execute(query, tuple(row))
                db.commit()
                print "db_updated"
            except MySQLdb.Error as e:
                db.rollback()
                print e
        cursor.close()
        print 'Done'


