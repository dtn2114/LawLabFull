#!/usr/bin/python
__author__ = 'bill'

import csv, datetime
import MySQLdb
from decimal import Decimal

if __name__ == '__main__':
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
    query = 'SELECT count(*) from bill_exec_0720 as a, bill_exec_0720 as b where a.cik = b.cik and a.ind_cik = b.ind_cik and a.year = b.year and a.total != b.total and a.salary != b.salary'
    cursor.execute(query)
    results = cursor.fetchall()
    print('salary ' + str(results))

    #bonus
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.bonus != b.bonus '
    cursor.execute(query)
    results = cursor.fetchall()
    print('bonus ' + str(results))

    #stock_awards
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.stock_awards != b.stock_awards '
    cursor.execute(query)
    results = cursor.fetchall()
    print('stock ' + str(results))

    #option_awards
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.option_awards != b.option_awards '
    cursor.execute(query)
    results = cursor.fetchall()
    print('option ' + str(results))

    #RSUs
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.RSUs != b.RSUs '
    cursor.execute(query)
    results = cursor.fetchall()
    print('RSUs ' + str(results))

    #nonequity_incentive_plan_compensation
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.nonequity_incentive_plan_compensation != b.nonequity_incentive_plan_compensation'
    cursor.execute(query)
    results = cursor.fetchall()
    print('nonequity ' + str(results))

    #change_in_pension_value_and_nonqualified_deferred_compensation
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.change_in_pension_value_and_nonqualified_deferred_compensation != b.change_in_pension_value_and_nonqualified_deferred_compensation'
    cursor.execute(query)
    results = cursor.fetchall()
    print('pension ' + str(results))

    #securities_underlying_options
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.securities_underlying_options != b.securities_underlying_options'
    cursor.execute(query)
    results = cursor.fetchall()
    print('securities ' + str(results))

    #all_other
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.all_other != b.all_other'
    cursor.execute(query)
    results = cursor.fetchall()
    print('all_other ' + str(results))

    #remainder
    query = 'SELECT count(*) from kate_thursday as a, kate_thursday as b where a.cik = b.cik and a.ind_cik = ' \
            'b.ind_cik and a.year = b.year and a.total != b.total and a.remainder != b.remainder'
    cursor.execute(query)
    results = cursor.fetchall()
    print('remainder ' + str(results))

    query = 'create table for_greg like bill_exec_0720; insert into for_greg select distinct c.* from bill_exec_0720 ' \
           'as c, (SELECT a.cik, a.accession from bill_exec_0720 as a, bill_exec_0720 as b where a.cik = b.cik and a.ind_cik = b.ind_cik and a.year = b.year and a.total != b.total and (a.total-b.total)/b.total > 1 group by a.year, a.accession having count(*)<2 limit 100) as d where c.cik = d.cik and c.accession = d.accession'
