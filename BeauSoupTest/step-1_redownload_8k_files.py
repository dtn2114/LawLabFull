#!/usr/bin/python
__author__ = 'bill'

import os, csv, datetime, re
import MySQLdb
import urllib2

if __name__ == '__main__':
    with open('missing_8k_files.txt', 'wb') as mf:
        mf.write('')
    with open('missing_8k_files_3.txt', 'rb') as f:
        # filenames = f.readlines()
        filenames = filter(None, (line.rstrip() for line in f))
        # print filenames[:10]

        path = 'http://www.sec.gov/Archives/'

        for i_filename, filename in enumerate(filenames):
            url = path + filename
            local_path = '/local/bill_test/edgar_8k/'
            # local_path = '/Users/bill/PycharmProjects/BeauSoupTest/'
            try:
                data = urllib2.urlopen(url).read()
                filename = '_'.join(filename.split('/'))
                filename = filename.split('.')[0]
                # print local_path+filename
                with open(local_path + filename + '.txt', 'wb') as f:
                    f.write(data)
                print "finished writing " + filename
                # filename = '/'.join(filename.split('_')) +'.txt'
                # print filename
            except Exception, e:
                print e
                with open('missing_8k_files.txt', 'a') as mf:
                    mf.write(filename +'\n')

