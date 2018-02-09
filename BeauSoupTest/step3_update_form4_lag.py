#!/usr/bin/python
__author__ = 'bill'

import os, csv, datetime, re
import MySQLdb
import urllib2
from decimal import *
import random
if __name__ == '__main__':
    print "getting list of distinct dates..."
    server_path = '/local/bill_test/insider/'
    with open(server_path + 'dates_2.csv', 'rb') as dates_file:
        dates_reader = csv.reader(dates_file)
        dates = [datetime.datetime.strptime(i[0], '%Y-%m-%d').date() for i in dates_reader]
    print "Number of distinct dates: %s" % len(dates)

    db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "bill")

    #filed_date is form4 filing date
    cursor = db.cursor()
    query = 'select transaction_date, filed_date, date from edgar_8k_form4_individual where formtype=4 group by ' \
            'transaction_date, filed_date, date'
    cursor.execute(query)
    main_results = cursor.fetchall()
    for i_result in range(len(main_results)):
        main_result = main_results[i_result]
        print "Processing " + str(i_result) + " out of " + str(len(main_results))
        transaction_date = main_result[0]
        filed_date = main_result[1]
        form_8k_date = main_result[2]

        if transaction_date in dates and filed_date in dates:
            form4_lag = str(dates.index(filed_date) - dates.index(transaction_date))
        else:
            form4_lag = None

        if transaction_date in dates and form_8k_date in dates:
            transaction_8k_lag = str(dates.index(form_8k_date) - dates.index(transaction_date))
        else:
            transaction_8k_lag = None

        query = 'update edgar_8k_form4_individual set form4_lag=%s, transaction_8k_lag=%s where transaction_date=%s ' \
                'and filed_date=%s and date=%s'
        cursor.execute(query, (form4_lag, transaction_8k_lag, transaction_date, filed_date, form_8k_date))
        db.commit()