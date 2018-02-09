#!/usr/bin/python
__author__ = 'bill'

import MySQLdb
if __name__ == '__main__':
    with open('step2_error.txt', 'w') as ef:
        ef.write('\n')
    db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "bill")
    cursor = db.cursor()

    sql = 'drop table edgar_8k_form4_individual'
    cursor.execute(sql)
    db.commit()
    print "drop old edgar_8k_form4_individual"
    sql = '''CREATE TABLE IF NOT EXISTS edgar_8k_form4_individual(
                        id BIGINT NOT NULL AUTO_INCREMENT,
                        tic TEXT,
                        date DATE,
                        event_date DATE,
                        filed_8k int(11),
                        lag int(11),
                        filename varchar(255),
                        contains_pr int(11),
                        personid int(11),
                        owner varchar(255),
                        transaction_date DATE,
                        num_shares_deriv DECIMAL(15,2),
                        filed_date DATE,
                        formtype int(11),
                        trancode char(1),
                        tprice decimal(15,4),
                        transaction_type int(5),
                        issuer_id bigint(20),
                        issuer_cik int(11),
                        accession varchar(255),
                        KEY(id)
              )'''
    cursor.execute(sql)
    db.commit()
    print "create table edgar_8k_form4_individual"

    query = 'create index tic on edgar_8k_form4_individual (tic(10))'
    cursor.execute(query)
    db.commit()

    query = 'create index issuer_id on edgar_8k_form4_individual (issuer_id)'
    cursor.execute(query)
    db.commit()

    query = 'create index issuer_cik on edgar_8k_form4_individual (issuer_cik)'
    cursor.execute(query)
    db.commit()

    query = 'create index accession on edgar_8k_form4_individual (accession(10))'
    cursor.execute(query)
    db.commit()
    print "create indexes"

    query = 'select tic, date, event_date, filed_8k, lag, filename, contains_pr from edgar_8k_form4 where ' \
            'total_insider_shares_lag > 0'
    cursor.execute(query)
    main_results = cursor.fetchall()
    for i_result in range(len(main_results)):
        main_result = main_results[i_result]
        print "Processing " + str(i_result) + " out of " + str(len(main_results))
        tic = main_result[0]
        date = main_result[1]
        event_date = main_result[2]
        filed_8k = main_result[3]
        lag = main_result[4]
        filename = main_result[5]
        contains_pr = main_result[6]


        query = 'INSERT INTO edgar_8k_form4_individual (tic,date,event_date,filed_8k,lag,filename,contains_pr,' \
                'PERSONID, OWNER, transaction_date,num_shares_deriv,filed_date,FORMTYPE, TRANCODE,TPRICE,' \
                'transaction_type, issuer_id, accession, issuer_cik) SELECT %s,%s,%s,%s,%s,%s, %s, owner_cik, ' \
                'owner_name,' \
                'transaction_date, transaction_shares, filing_date , form_type, transaction_code,' \
                'transaction_price, 1, issuer_id, accession, issuer_cik FROM non_derivative2 WHERE transaction_date ' \
                '>= %s AND ' \
                'transaction_date < %s ' \
                'AND TICKER=%s AND LENGTH(TRIM(transaction_shares))>0'
        cursor.execute(query, (tic,date,event_date,filed_8k,lag,filename,contains_pr,event_date, date, tic))
        db.commit()


    query = 'select tic,date,event_date,filed_8k,lag,filename, contains_pr from edgar_8k_form4 where ' \
            'total_insider_shares_lag=0'
    cursor.execute(query)
    main_results = cursor.fetchall()
    for i_result in range(len(main_results)):
        main_result = main_results[i_result]
        print "Processing " + str(i_result) + " out of " + str(len(main_results))
        tic = main_result[0]
        date = main_result[1]
        event_date = main_result[2]
        filed_8k = main_result[3]
        lag = main_result[4]
        filename = main_result[5]
        contains_pr = main_result[6]

        query = 'INSERT INTO edgar_8k_form4_individual (tic, date,event_date,filed_8k,lag,filename,contains_pr,' \
                'PERSONID, OWNER, transaction_date,num_shares_deriv, filed_date, issuer_id, accession, ' \
                'issuer_cik) SELECT %s,%s,%s,%s,%s,%s, %s, ' \
                'PERSONID, OWNER, NULL, 0, NULL, issuer_id, accession, issuer_cik FROM ' \
                'edgar_8k_form4_individual where tic=%s AND PERSONID NOT IN (SELECT PERSONID FROM ' \
                'edgar_8k_form4_individual WHERE date=%s AND tic=%s) GROUP BY PERSONID'

        cursor.execute(query, (tic,date,event_date,filed_8k,lag,filename,contains_pr,tic,date,tic))
        db.commit()