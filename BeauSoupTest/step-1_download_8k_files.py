#!/usr/bin/python
__author__ = 'bill'

import os, csv, datetime, re
import MySQLdb
import urllib2

if __name__ == '__main__':
    with open('missing_8k_files.txt', 'wb') as mf:
        mf.write('')
    db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "bill")
    cursor = db.cursor()
    query = "select distinct filename from edgar_8k"
    cursor.execute(query)
    print "create a list of all filenames"
    filenames = cursor.fetchall()
    for filename in filenames:
        print "processing " + str(filename[0]) + "..."
        filename = str(filename[0])
        path = 'http://www.sec.gov/Archives/'
        url = path + filename
        local_path = '/local/bill_test/edgar_8k/'
        try:
            data = urllib2.urlopen(url).read()
            filename = '_'.join(filename.split('/'))
            with open(local_path+filename, 'wb') as f:
                f.write(data)
            print "finished writing " + filename
            filename = '/'.join(filename.split('_'))
        except Exception, e:
            print e
            with open('missing_8k_files.txt', 'a') as mf:
                mf.write(filename + '\n')