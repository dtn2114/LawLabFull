#!/usr/bin/python

import csv
import MySQLdb
import pandas as pd
import sqlalchemy
import numpy as np

def print_row(data):
    for row in data:
        print len(row),row

if __name__ == '__main__':
    # path = '/Users/bill/PycharmProjects/BeauSoupTest/'
    path = '/local/bill_test/'
    df = pd.read_csv(path + 'execucomp2.csv')
    # print(df.columns)

    # df['cshoq'] = df.groupby(['tic'])['cshoq'].transform(lambda grp: grp.fillna(method='ffill'))

    df['SALARY'] = df['SALARY']*1000
    df['BONUS'] = df['BONUS']*1000
    df['STOCK_AWARDS'] = df['STOCK_AWARDS']*1000
    df['OPTION_AWARDS'] = df['OPTION_AWARDS']*1000
    df['PENSION_CHG'] = df['PENSION_CHG']*1000
    df['RSTKGRNT'] = df['RSTKGRNT']*1000
    df['ALLOTHTOT'] = df['ALLOTHTOT']*1000
    df['TOTAL_SEC'] = df['TOTAL_SEC']*1000
    df = df.astype(object).where(pd.notnull(df), None)
    # print df2.iloc[:2]
    # df.to_sql
    A = df.values.tolist()
    # print_row(A[:4])

    db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "def14a")
    cursor = db.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS exec_comp_wharton(
                        id BIGINT NOT NULL AUTO_INCREMENT,
                        name TEXT,
                        co_per_rol TEXT,
                        year INT(11),
                        coname TEXT,
                        salary DECIMAL(19,2),
                        bonus DECIMAL(19,2),
                        stock_awards DECIMAL(19,2),
                        option_awards DECIMAL(19,2),
                        pension_chg DECIMAL(19,2),
                        total_sec DECIMAL(19,2),
                        RSUs DECIMAL(19,2),
                        all_other DECIMAL(19,2),
                        gvkey INT(11),
                        CUSIP VARCHAR(255),
                        ticker TEXT,
                        KEY(id)
              )'''
    cursor.execute(sql)
    query = "INSERT INTO exec_comp_wharton(`name`, `co_per_rol`, `coname`, `salary`, `bonus`, `stock_awards`,`option_awards`,`pension_chg`, `total_sec`, `RSUs`, `all_other`, `gvkey`,`year`, `cusip`, `ticker`)"\
                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # # print_row()
    # for i, row in enumerate(A):
    #     for j, cell in enumerate(row):
    #         if 'nan' in str(cell):
    #             A[i][j] = None
    #         else:
    #             pass
    for row in A:
        try:
            cursor.execute(query, tuple(row))
            db.commit()
            print "db_updated"
        except MySQLdb.Error as e:
            db.rollback()
            print e
    print 'Done'


    # conn = sqlalchemy.engine.Connection()
    # cursor = db.cursor()
    # df[150:151].to_sql(con=db, name='market_cap_two2', if_exists='replace', flavor='mysql', dtype={'cshoq':
    #                                                                                                   sqlalchemy.types.DECIMAL})
    # df2[:150].to_sql(con=db, name='market_cap_two2', if_exists='append', flavor='mysql')
    # df2[151:].to_sql(con=db, name='market_cap_two2', if_exists='append', flavor='mysql')
    # df.to_sql(con=db, name='market_cap_two2', if_exists='replace', flavor='mysql', dtype={'cshoq':
    # sqlalchemy.DECIMAL})

    #
    # sql = '''CREATE TABLE IF NOT EXISTS mket_caps_0601(
    #                     id BIGINT NOT NULL AUTO_INCREMENT,
    #                     date DATE,
    #                     ticker TEXT,
    #                     price_per_share DECIMAL(19,2)
    #                     outstanding_share_1 DECIMAL(19,2)
    #                     outstanding_share_2 DECIMAL(19,2)
    #                     cik INT(11)
    #                     sic INT(11)
    #                     KEY(id)
    #           )'''
    #
    # cursor.execute(sql)
    # print 'Table created'
    # query = "INSERT INTO mket_caps_0601(`date`, `ticker`, `price_per_share`, `outstanding_share_1`," \
    #         "`outstanding_share_2`, `cik`, `sic`, " \
    #             "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"

    # with open(path + 'two_mket_caps.csv', 'r') as file:
    #
    #     reader = csv.reader(file)
    #     # row_count = sum(1 for row in reader)
    #     row_count = 2493513;
    #     i = 0
    #     # print row_count
    #     for i, row in enumerate(reader):
    #         row = row[2:]
    #         print row
    #         if i >20:
    #             break
    #         else:
    #             pass
    #         # try:
    #         #     cursor.execute(query, tuple(row))
    #         #     db.commit()
    #         #     print "db_updated"
    #         # except MySQLdb.Error as e:
    #         #     db.rollback()
    #         #     print e
    #         # print 'Done'


