#!/usr/bin/python
__author__ = 'bill'

import os, csv, datetime, re
import MySQLdb
import urllib2

if __name__ == '__main__':
    with open('step0b_error_files.txt', 'wb') as ef:
        ef.write('')
    db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "bill")
    cursor = db.cursor()

    query = 'alter table edgar_8k drop column contains_502, drop column contains_under, drop column ' \
            'contains_pr, drop column pr_date, drop column contains_10b51, drop column ' \
            'contains_103, drop column contains_202, drop column contains_701'
    cursor.execute(query)
    db.commit()

    query = 'alter table edgar_8k add column contains_502 INT(11), add column contains_under INT(11), add column ' \
            'contains_pr INT(11), add column pr_date date, add column contains_10b51 INT(11), add column ' \
            'contains_103 INT(11), add column contains_202 INT(11), add column contains_701 INT(11)'
    cursor.execute(query)
    db.commit()
    print "add columns"
    query = 'select distinct filename from edgar_8k where event_date is not null and date_filed >= "2004-07-01" and event_date >= "2004-04-01" '
    cursor.execute(query)
    main_results = cursor.fetchall()
    print "get all filenames"
    months_of_the_year_regex = "january|february|march|april|may|june|july|august|september|october|november|december"
    for i_result, main_result in enumerate(main_results):
        print "Processing " + str(i_result) + " out of " + str(len(main_results))
        filename = main_result[0]
        if filename is not None:
            # path = 'http://www.sec.gov/Archives/'
            path = '/local/bill_test/edgar_8k/'
            filename = '_'.join(filename.split('/'))
            url = path + filename
            print "Processing " + filename
            # raw_text = urllib2.urlopen(url).read()
            try:
                with open(url, 'r') as f:
                    raw_text = f.read()
                filename = '/'.join(filename.split('_'))
                raw_text = raw_text.lower()
                contains_502 = raw_text.find('5.02') > -1
                contains_under = raw_text.find('underwriting') > -1 or raw_text.find('unregistered') > -1
                contains_pr = raw_text.find('press release') > -1
                contains_10b51 = raw_text.find('10b5-1') > -1
                contains_103 = raw_text.find('1.03') > -1
                contains_202 = raw_text.find('2.02') > -1
                contains_701 = raw_text.find('7.01') > -1

                print "Found the contains"

                pr_date = None
                if contains_pr:
                    date_match = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december) ([0-9]{1,2}),* '
                                           r'(20[0-9][0-9]) .*?press release', raw_text)
                # print date_match
                    if date_match is not None:
                        pr_date = datetime.datetime.strptime(date_match.group(1) + ' ' + date_match.group(2) + ' ' + date_match.group(3), '%B %d %Y' )
                    else:
                        date_match = re.search(r'press release.*?(january|february|march|april|may|june|july|august|september|october|november|december) ([0-9]{1,2})'
                                           r',* (20[0-9][0-9])', raw_text, re.DOTALL)
                        if date_match is not None:
                            pr_date = datetime.datetime.strptime(date_match.group(1) + ' ' + date_match.group(2) + ' ' +
                                                                 date_match.group(3), '%B %d %Y')
                query = 'UPDATE edgar_8k set contains_502=%s, contains_under=%s, contains_pr=%s, pr_date=%s, ' \
                        'contains_10b51=%s, contains_103=%s,contains_202=%s, contains_701=%s where filename=%s'
                cursor.execute(query, (contains_502, contains_under, contains_pr, pr_date, contains_10b51,
                                       contains_103, contains_202, contains_701, filename))
                db.commit()
                print 'updated the contains'

            except Exception, e:
                print e
                with open('step0b_error_files.txt', 'a') as ef:
                    ef.write(filename + '\n')

            # pr_date = None
            # if contains_pr:
            #     date_match = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december) ([0-9]{1,2}),* '
            #                            r'(20[0-9][0-9]) .*?press release', raw_text)
            #     # print date_match
            #     if date_match is not None:
            #         pr_date = datetime.datetime.strptime(date_match.group(1) + ' ' + date_match.group(2) + ' ' + date_match.group(3), '%B %d %Y' )
            #     else:
            #         date_match = re.search(r'press release.*?(january|february|march|april|may|june|july|august|september|october|november|december) ([0-9]{1,2})'
            #                                r',* (20[0-9][0-9])', raw_text, re.DOTALL)
            #         if date_match is not None:
            #             pr_date = datetime.datetime.strptime(date_match.group(1) + ' ' + date_match.group(2) + ' ' +
            #                                                  date_match.group(3), '%B %d %Y')
            # query = 'UPDATE edgar_8k set contains_502=%s, contains_under=%s, contains_pr=%s, pr_date=%s, ' \
            #         'contains_10b51=%s, contains_103=%s,contains_202=%s, contains_701=%s where filename=%s'
            # cursor.execute(query, (contains_502, contains_under, contains_pr, pr_date, contains_10b51,
            #                        contains_103, contains_202, contains_701, filename))
            # db.commit()
            # print 'updated the contains'





