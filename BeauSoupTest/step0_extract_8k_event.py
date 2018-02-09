#!/usr/bin/python
__author__ = 'bill'

import os, csv, datetime, re
import MySQLdb
import urllib2

def extract_8K_event_date(filename, db):
    path = 'http://www.sec.gov/Archives/'
    url = path + filename
    try:
        data = urllib2.urlopen(url).read()
        search_match = re.search('CONFORMED PERIOD OF REPORT:\s*([0-9]+)', data)
        if search_match:
            try:
                event_date = search_match.group(1)
                event_date = datetime.datetime.strptime(event_date, '%Y%m%d')
                query = 'update edgar_8k set event_date = %s where filename = %s'
                cursor = db.cursor()
                print filename
                cursor.execute(query, (event_date.strftime('%Y-%m-%d'), filename))
                db.commit()
                print query % (event_date.strftime('%Y-%m-%d'), filename.strip())
                # print 'edgar_8k updated'
            except MySQLdb.Error as e:
                db.rollback()
                print e
        else:
            with open('8k_error.txt', 'a') as ef:
                ef.write(filename + ' :No event_date found' + '\n')
                print "No event_date found"

        # print "No event date"
    except Exception as e:
        print e
        with open('8k_error.txt', 'a') as ef:
            ef.write(filename + ' :No 8k.txt files found' + '\n')
            print "No 8k.txt found"


if __name__ == '__main__':
    with open('8k_error.txt', 'w') as ef:
        ef.write('\n')
    db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "bill")
    cursor = db.cursor()

    # query = 'alter table edgar_8k drop table event_date DATE'
    # cursor.execute(query)
    # db.commit()
    # print "add event_date column"

    query = 'alter table edgar_8k add event_date DATE'
    cursor.execute(query)
    db.commit()
    print "add event_date column"

    query = "select distinct filename from edgar_8k"
    cursor.execute(query)
    print "create a list of all filename"
    filenames = cursor.fetchall()
    for filename in filenames:
        print "processing " + str(filename[0]) + "..."
        extract_8K_event_date(str(filename[0]), db)

