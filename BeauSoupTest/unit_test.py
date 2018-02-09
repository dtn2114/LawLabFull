#!/usr/bin/python
__author__ = 'bill'

import MySQLdb
import re
import datetime
import urllib2
import numpy as np
import subprocess


def  getIntegerComplement(n):
    x = "{0:b}".format(n)
    y = ''.join(str(1-int(i))for i in x)
    return int(y,2)

def  maxDifference( a):
    #for i in range(len(a)):
    cur_max = max(a)
    cur_min = min(a)
    #print cur_max, cur_min
    if len(a) <= 1:
        return -1
    if a.index(cur_max)== 0:
        a.remove(cur_max)
        #print a
        return maxDifference(a)
    elif a.index(cur_max) <= a.index(cur_min):
        a.remove(cur_min)
        #print a
        return maxDifference(a)
    else:
        return cur_max - cur_min


def verticle_flow(a):
    for i in range(len(a[1,:])):
        b = a[:,i]
        loc = np.nonzero(b == 0)
        print loc
        if len(loc[0]) != 0:
            loc = loc[0][0]
            print loc
            a[loc:len(a[:,1]),i] = 0
        else:
            pass
    return a

if __name__ == '__main__':
    with open('finra.txt', 'rb') as f:
        crds = [x.strip('\n') for x in f.readlines()]
    for i in crds[:2]:
        # print i
        cmd = 'curl -s http://brokercheck.finra.org/Individual/Summary/' + i
        output = subprocess.check_output(cmd, shell = True)
        print output
    # a = np.array([[0,1,0,1],[0,1,1,1], [0,0,1,1], [0,0,1,1]])
    # print(a, len(a))
    # a = verticle_flow(a)
    # print(a)

    # db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "website")
    # cursor = db.cursor()
    #
    # # query = 'alter table greentaxi add index(passenger_count)'
    # # cursor.execute(query)
    # # db.commit()
    # # print 'add greentaxi passenger_count'
    # #
    # # query = 'alter table greentaxi add index(total_amount)'
    # # cursor.execute(query)
    # # db.commit()
    # # print 'add greentaxi total_amount'
    # #
    # # query = 'alter table greentaxi add index(tpep_pickup_datetime)'
    # # cursor.execute(query)
    # # db.commit()
    # # print 'add greentaxi tpep_pickup_datetime'
    # #
    # # query = 'alter table yellowtaxi add index(VendorID)'
    # # cursor.execute(query)
    # # db.commit()
    # # print 'add yellow VendorID'
    # #
    # # query = 'alter table yellowtaxi add index(passenger_count)'
    # # cursor.execute(query)
    # # db.commit()
    # # print 'add yellow passenger_count'
    # #
    # # query = 'alter table yellowtaxi add index(total_amount)'
    # # cursor.execute(query)
    # # db.commit()
    # # print 'add yellow total_amount'
    #
    # query = 'alter table yellowtaxi add index(pickup_longitude)'
    # cursor.execute(query)
    # db.commit()
    # print 'add yellow longitude'
    #
    # query = 'alter table yellowtaxi add index(pickup_latitude)'
    # cursor.execute(query)
    # db.commit()
    # print 'add yellow latitude'
    #
    # db.close()
    # url = 'http://www.sec.gov/Archives/edgar/data/1013238/0000891092-04-004981.txt'
    # raw_text = urllib2.urlopen(url).read()
    # # filename = 'edgar_data_1013238_0000891092-04-004981.txt'
    # # with open(filename, 'rb') as f:
    # #     raw_text = f.read()
    #
    # # print raw_text
    # # filename = '/'.join(filename.split('_'))
    # raw_text = raw_text.lower()
    #
    # date_match = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december) ([0-9]{1,2}),* '
    #                        r'(20[0-9][0-9]) .*?press release', raw_text)
    # # print date_match
    # if date_match is not None:
    #     pr_date = datetime.datetime.strptime(date_match.group(1) + ' ' + date_match.group(2) + ' ' +
    #                                           date_match.group(3), '%B %d %Y' )
    #     # print pr_date
    # else:
    #     date_match = re.search(r'press release.*?(january|february|march|april|may|june|july|august|september|october|november|december) ([0-9]{1,2})'
    #                        r',* (20[0-9][0-9])', raw_text, re.DOTALL)
    #     print date_match.group(0)
    #     if date_match is not None:
    #         pr_date = datetime.datetime.strptime(date_match.group(1) + ' ' + date_match.group(2) + ' ' +
    #                                              date_match.group(3), '%B %d %Y')
    #         # print pr_date