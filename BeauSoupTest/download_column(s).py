#!/usr/bin/python
__author__ = 'bill'

import re, MySQLdb, csv, pandas as pd
from decimal import Decimal

#Insert a CSV into a SQL table.

def print_row(data):
    for row in data:
        print len(row),row

if __name__ == '__main__':
    path = '/local/bill_test/'
    df = pd.read_csv(path + '0731stockprices.csv')
    df = df.astype(object).where(pd.notnull(df), None)
    # print_row(df[:4])
    df = df.drop('PERMNO', 1)

    A = df.values.tolist()
    A = tuple([tuple(a) for a in A])
    # print_row(A[:4])
    # print A[:4]
    db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "bill")
    cursor = db.cursor()
    sql = 'drop table transprice3'
    cursor.execute(sql)
    sql = '''CREATE TABLE IF NOT EXISTS transprice3(
                        tic TEXT,
                        prccd DECIMAL(19,4),
                        caldt date
        )'''
    cursor.execute(sql)
    query = "create index tic on transprice3(tic(4))"
    cursor.execute(query)
    query = "create index prccd on transprice3(prccd)"
    cursor.execute(query)
    query = "create index caldt on transprice3(caldt)"
    cursor.execute(query)

    query = "INSERT INTO transprice3(`caldt`, `tic`, `prccd`)"\
                    "VALUES(%s, %s, %s)"
    cursor.executemany(query, A)
    db.commit()
    # for row in A:
    #     print "Processing " + str(Decimal(A.index(row))/Decimal(len(A))) + "% " + " out of 100% for total of " + str(
    #         len(A))
    #     cursor.execute(query, tuple(row[1:]))
    #     db.commit()
        # print "db_updated"
    # print 'Done'
    db.close()
# #Download a Column into a text file
# if __name__ == '__main__':
#     db = MySQLdb.connect("localhost", "root", "Edgar20!4", "bill")
#     cursor = db.cursor()
#     query = 'select distinct tic from edgar_8k_form4_individual'
#     cursor.execute(query)
#     results = cursor.fetchall()
#     with open('tic_list.txt', 'w') as f:
#         for i_results in range(len(results)):
#             result = results[i_results]
#             tic = result[0]
#             f.write(tic+ '\n')

