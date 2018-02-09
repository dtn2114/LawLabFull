#!/usr/bin/python
__author__ = 'bill'

import os, csv, datetime, re
import MySQLdb
import urllib2
from decimal import Decimal
import random
if __name__ == '__main__':
    # with open('step1_error.txt', 'w') as ef:
    #     ef.write('\n')
    db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "bill")
    cursor = db.cursor()
    sql = 'drop table edgar_8k_form4'
    cursor.execute(sql)
    db.commit()
    sql = '''CREATE TABLE IF NOT EXISTS edgar_8k_form4(
                        id BIGINT NOT NULL AUTO_INCREMENT,
                        tic VARCHAR(255),
                        date DATE,
                        marketcap int(11),
                        event_date DATE,
                        filed_8k int(11),
                        lag int(11),
                        filename varchar(255),
                        contains_pr int(11),
                        total_insider_shares_lag DECIMAL(11,2),
                        KEY(id)
              )'''
    cursor.execute(sql)
    db.commit()
    print "create table edgar_8k_form4"

    # path = 'Users/bill/PycharmProjects/BeauSoupTest/insider/'
    server_path = '/local/bill_test/insider/'
    with open(server_path + 'tics_marketcap.csv', 'rb') as f:
        tics_reader = csv.reader(f)
        tics = []
        marketcaps = {}
        for i in tics_reader:
            tics.append(i[0].upper())
            try:
                marketcaps[i[0]] = long(Decimal(i[1]))
            except Exception, e:
                marketcaps[i[0]] = None

    # query = 'select distinct tic from edgar_8k'
    # cursor.execute(query)
    # tics = cursor.fetchall()
    # tics = [i[0] for i in tics]

    print "Number of distinct tickers : %s" % len(tics)

    with open(server_path + 'dates_2.csv', 'rb') as date_f:
        dates_reader = csv.reader(date_f)
        dates = [datetime.datetime.strptime(i[0], '%Y-%m-%d').date() for i in dates_reader]
    print "Number of distinct date: %s " % len(dates)

    # i_tic = 1
    for i_tic in range(len(tics)):
        tic = tics[i_tic]
        print "PROCESSING TICKER: %s, %s out of %s" % (tic, str(i_tic), str(len(tics)))
        query = "select date_filed, pr_date, event_date, filename, contains_pr from edgar_8k where contains_502 = 0 " \
                "and contains_under = 0 and contains_10b51 = 0 and contains_103 = 0 and  contains_202=0 and " \
                "contains_701=0 and tic = %s and " \
                "event_date is not null " \
                "and date_filed >= '2004-07-01' AND event_date >= '2004-04-01' group by date_filed"
        cursor.execute(query, (tic,))
        results = cursor.fetchall()
        filing_dates_8k = [i[0] for i in results]
        pr_dates = [i[1] for i in results]
        event_dates_8k = [i[2] for i in results]
        filenames = [i[3] for i in results]
        contains_prs = [i[4] for i in results]
        print "Get all the filling_dates_8k, pr_dates, event_dates_8k, filenames"

        #This replace the filing_dates with pr_dates when pr_dates is before filing_dates
        for i_filing_date_8k in range(len(filing_dates_8k)):
            if pr_dates[i_filing_date_8k] is not None and pr_dates[i_filing_date_8k] in dates and pr_dates[i_filing_date_8k] < filing_dates_8k[i_filing_date_8k] and pr_dates[i_filing_date_8k] >= event_dates_8k[i_filing_date_8k]:
                filing_dates_8k[i_filing_date_8k] = pr_dates[i_filing_date_8k]
                # print "replacing the " +  str(i_filing_date_8k) + "th in " + str(len(filing_dates_8k)) + " filing_dates"

        #The following script creates a control group
        #It takes the last a random segment of dates in the last quarters
        # that matches each event date and its filing date.
        filing_dates_non_8k = []
        for filing_date_8k in filing_dates_8k:
            if filing_date_8k.month >= 1 and filing_date_8k.month <= 3:
                last_quarter_month_start = 9
                last_quarter_day_start = 30
                last_quarter_month_end = 12
                last_quarter_day_end = 31
                last_quarter_year = filing_date_8k.year - 1
            if filing_date_8k.month >= 4 and filing_date_8k.month <= 6:
                last_quarter_month_start = 1
                last_quarter_day_start = 31
                last_quarter_month_end = 3
                last_quarter_day_end = 31
                last_quarter_year = filing_date_8k.year
            if filing_date_8k.month >= 7 and filing_date_8k.month <= 9:
                last_quarter_month_start = 4
                last_quarter_day_start = 30
                last_quarter_month_end = 6
                last_quarter_day_end = 30
                last_quarter_year = filing_date_8k.year
            if filing_date_8k.month >= 10 and filing_date_8k.month <= 12:
                last_quarter_month_start = 7
                last_quarter_day_start = 31
                last_quarter_month_end = 9
                last_quarter_day_end = 30
                last_quarter_year = filing_date_8k.year

            last_quarter_start = datetime.date(last_quarter_year, last_quarter_month_start, last_quarter_day_start)
            last_quarter_end = datetime.date(last_quarter_year, last_quarter_month_end, last_quarter_day_end)

            last_quarter_dates = [x for x in dates if x >= last_quarter_start and x <= last_quarter_end]
            potential_dates = [x for x in last_quarter_dates if x not in filing_dates_8k and x not in filing_dates_non_8k]
            if len(potential_dates) == 0:
                potential_dates = [x for x in dates if x not in filing_dates_8k and x not in filing_dates_non_8k]

            filing_dates_non_8k += random.sample(potential_dates, 1)


        event_dates_non_8k = []
        for i_filing_date_non_8k in range(len(filing_dates_non_8k)):
            filing_date_non_8k = filing_dates_non_8k[i_filing_date_non_8k]
            # print "Processing the " + str(i_filing_date_non_8k) + "th in " + str(len(filing_dates_non_8k))
            event_date_8k = event_dates_8k[i_filing_date_non_8k]

            i_trial = 0
            while event_date_8k not in dates and i_trial < 10:
                event_date_8k = event_date_8k - datetime.timedelta(days=1)
                i_trial += 1

            i_lag = dates.index(filing_dates_8k[i_filing_date_non_8k]) - dates.index(event_date_8k)
            event_date_index = dates.index(filing_date_non_8k) - i_lag

            if event_date_index >=0:
                event_date = dates[event_date_index]
            else:
                event_date = dates[0]
            event_dates_non_8k += [event_date]

        all_filing_dates = filing_dates_8k + filing_dates_non_8k
        all_event_dates = event_dates_8k + event_dates_non_8k

        print "Number of all dates: " + str(len(all_filing_dates))


        for i_date in range(len(all_filing_dates)):
            date = all_filing_dates[i_date]
            # print "Processing the " + str(i_date) + "th in " + str(len(all_filing_dates)) + " all filing dates"
            filed_8k = i_date < len(filing_dates_8k)
            event_date = all_event_dates [i_date]

            i_trial = 0
            while event_date not in dates and i_trial < 10:
                event_date = event_date - datetime.timedelta(days=1)
                i_trial += 1

            if event_date in dates and date in dates:
                lag = str(dates.index(date) - dates.index(event_date))
            else:
                lag = '.'

            if filed_8k:
                filename= filenames[i_date]
                contains_pr = contains_prs[i_date]
            else:
                filename = None
                contains_pr = None

            query = 'select transaction_shares, filing_date from non_derivative2 where transaction_date >= %s and ' \
                    'transaction_date < %s and ticker = %s'
            cursor.execute(query, (event_date, date, tic))
            results = cursor.fetchall()
            total_insider_shares = sum([Decimal(l[0]) for l in results if l[0] is not None and len(str(l[0])) > 0])

            query = 'insert into edgar_8k_form4 (tic, date, marketcap, filed_8k, event_date, lag, filename, ' \
                    'contains_pr, total_insider_shares_lag) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) '
            try:
                cursor.execute(query, (tic,date.strftime('%Y-%m-%d'), marketcaps[tic] ,int(filed_8k),
                                       event_date.strftime("%Y-%m-%d"),lag,filename,contains_pr,total_insider_shares))
                db.commit()
            except Exception, e:
                print str(e)
