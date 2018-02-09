#!/usr/bin/python
__author__ = 'bill'

import csv, datetime
import MySQLdb
from decimal import Decimal

if __name__ == '__main__':
    server_path = '/local/bill_test/insider/'
    with open(server_path + 'dates_2.csv', 'rb') as date_f:
        dates_reader = csv.reader(date_f)
        dates = [datetime.datetime.strptime(i[0], '%Y-%m-%d').date() for i in dates_reader]
    print "Number of distinct date: %s " % len(dates)



    # db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "insider")
    # cursor = db.cursor()
    # query = 'SELECT tic, prccd, caldt from insider.transprice2'
    # cursor.execute(query)
    # transprice_results = cursor.fetchall()
    # transprice_results = [list(transprice_result) for transprice_result in transprice_results]
    # print transprice_results
    # db.close()

    db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "bill")
    cursor = db.cursor()
    query = 'SELECT id, tic, transaction_date, date from edgar_8k_form4_individual'
    cursor.execute(query)
    main_results = cursor.fetchall()


    with open('error_executive_comp.txt', 'w') as ef:
        ef.write('')
    a = int(0)
    b = int(len(main_results))
    for i_result in range(a,b):
        try:
            main_result = main_results[i_result]
            print "Processing " + str(i_result) + " in the range from " + str(a) + " to " + str(b)
            id = main_result[0]
            tic = main_result[1]
            transaction_date = main_result[2]
            date = main_result[3]
            if date in dates:
                i_form8k_filing_date = dates.index(date)
                form8k_filing_date = dates[i_form8k_filing_date+1]
            else:
                with open('error_executive_comp.txt', 'a') as ef:
                    ef.write(str(id) + ' no date' + '\n')
                form8k_filing_date = date

            db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "bill")
            cursor = db.cursor()
            query = 'SELECT prccd from transprice4 where tic = %s and caldt = %s'
            cursor.execute(query, (tic, form8k_filing_date))
            transprice_results = cursor.fetchall()
            print transprice_results, form8k_filing_date, tic
            transprice_results = [Decimal(transprice_results[0][0]) if transprice_results else None]
            print transprice_results
            if transprice_results[0]:

                db.close()
                db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "bill")
                cursor = db.cursor()
                query = 'select vwretx from sp where caldt > %s and caldt <=%s'
                cursor.execute(query, (transaction_date, date))
                market_change = cursor.fetchall()
                # print market_change
                market_change = sum([Decimal(l[0]) if l[0] is not None and len(str(l[0])) > 0 else Decimal(0) for l in
                                     market_change ])
                # print market_change

                print id, transprice_results, market_change
                db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "bill")
                cursor = db.cursor()
                query = 'update edgar_8k_form4_individual set form8k_filing_prc_tplus1 = %s, marketchange=%s where id = %s'
                cursor.execute(query, (transprice_results[0], market_change, id))
                db.commit()
                print "updated"
            else:
                print "Next loop"
                continue
        # raise SystemExit(0)
        except Exception, e:
            print "ERROR MESSAGE: "+ str(id) + ' ' + str(e)
            with open('error_executive_comp.txt', 'ab') as ef:
                ef.write(str(id) +' ' + str(e) + '\n')


def investigate_def14a():
    db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "def14a")
    cursor = db.cursor()
    # find companies that doesn't have any ind_cik
    # query = 'select distinct cik from bill_exec_0720_copy as a where a.cik not in (select cik from bill_exec_0720_copy where ind_cik is not null)'
    # cursor.execute(query)
    # # check if these companies are in reporters_345
    # query = 'select distinct issuer_cik from reporters_345 as b where b.cik not in (select distinct cik from ' \
    #         'def14a.bill_exec_0720_copy as a where a.cik not in (select cik from def14a.bill_exec_0720_copy where ' \
    #         'ind_cik is not null))'
    #
    # query = 'selectyeeu  distinct cik from def14a.bill_exec_0720_copy as a where a.cik not in (select cik from
    # def14a.bill_exec_0720_copy where ind_cik is not null)'

    #total
    query = 'SELECT a.* from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = b.ind_cik and a.year = b.year and a.total != b.total'
    cursor.execute(query)
    results = cursor.fetchall()
    print('total different rows ' + str(len(results)))

    #salary
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = b.ind_cik and a.year = b.year and a.total != b.total and a.salary != b.salary'
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)

    #bonus
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.bonus != b.bonus '
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)

    #stock_awards
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.stock_awards != b.stock_awards '
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)

    #option_awards
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.option_awards != b.option_awards '
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)

    #RSUs
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.RSUs != b.RSUs '
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)

    #nonequity_incentive_plan_compensation
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.nonequity_incentive_plan_compensation != b.nonequity_incentive_plan_compensation'
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)

    #change_in_pension_value_and_nonqualified_deferred_compensation
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.change_in_pension_value_and_nonqualified_deferred_compensation != b.change_in_pension_value_and_nonqualified_deferred_compensation'
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)

    #securities_underlying_options
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.securities_underlying_options != b.securities_underlying_options'
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)

    #all_other
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.all_other != b.all_other'
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)

    #remainder
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.remainder != b.remainder'
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)