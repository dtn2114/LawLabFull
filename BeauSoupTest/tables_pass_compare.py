#!/usr/bin/python

import glob
import os
import MySQLdb
import datetime

if __name__ == '__main__':
    # # path = '/local/def14a_extract/tables_dates/'
    # # path = '/Users/bill/PycharmProjects/BeauSoupTest/textfiles/tables_pass_three/'
    # #print glob.glob(path)
    # path = '/local/def14a_extract/tables_pass_three2/'
    # configfiles = [os.path.join(dirpath, f) for dirpath, dirnames, files in os.walk(path) for f in files if f.endswith('.txt')]
    # #This extract the unique cik and accession of all the files in exec_comp_finals
    # # print configfiles
    # tables_pass_three =[]
    # txtpath = ''
    # with open(txtpath+'tables_pass_three2.txt', 'w') as ef:
    #     for filepath in configfiles:
    #         filename = filepath.split('/')[-1]
    #         filename = filename.split('_')
    #         # print filename
    #         accession_exec = filename[0]
    #         cik_exec = filename[1].split('.')[0]
    #         cik_accession_exec = '_'.join([cik_exec, accession_exec])
    #         tables_pass_three.append(cik_accession_exec)
    #         ef.write(cik_accession_exec + '\n')
    # tables_pass_three = set(tables_pass_three)
    # print len(tables_pass_three)

    path = '/local/bill_test/exec_comp_tables_final/'
    configfiles = [os.path.join(dirpath, f) for dirpath, dirnames, files in os.walk(path) for f in files if f.endswith('.txt')]
    #This extract the unique cik and accession of all the files in exec_comp_finals
    # print configfiles
    exec_comp_tables_final =[]
    txtpath = ''
    with open(txtpath+'tables_pass_three_0606.txt', 'w') as ef:
        for filepath in configfiles:
            filename = filepath.split('/')[-1]
            filename = filename.split('_')
            # print filename
            accession_exec = filename[0]
            cik_exec = filename[1].split('.')[0]
            cik_accession_exec = '_'.join([cik_exec, accession_exec])
            exec_comp_tables_final.append(cik_accession_exec)
            ef.write(cik_accession_exec + '\n')
    exec_comp_tables_final = set(exec_comp_tables_final)
    print len(exec_comp_tables_final)


    # path = '/local/def14a_extract/tables_dates/'
    # configfiles2 = [os.path.join(dirpath, f)
    #                for dirpath, dirnames, files in os.walk(path)
    #                for f in files if f.endswith('.txt')]
    # # ALL FILING FROM TABLES_DATE FOLDER
    # all_filing = []
    # txtpath = ''
    # with open(txtpath + 'tables_date_0601.txt', 'w') as tf:
    #     tf.write("ALL cik, accession FROM TABLE_DATES \n")
    #     for filepath in configfiles2:
    #         filename = filepath.split('/')[-2:]
    #         cik = filename[0]
    #         accession_filedate = filename[1].split('.')[0].split('_')
    #         # print accession_filedate
    #         accession = accession_filedate[0]
    #         file_date = accession_filedate[1]
    #         cik_accession = '_'.join([cik, accession])
    #         # cik_accession_year.extend([cik,accession,file_year])
    #         all_filing.append(cik_accession)
    #         tf.write(cik_accession + '\n')
    # print len(set(all_filing))
    # # print all_filing


    # GET CIK, ACCESSION from the tables
    db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "def14a")
    cursor = db.cursor()
    query = '''SELECT DISTINCT cik, accession FROM bill_exec_0606'''
    cursor.execute(query)
    all_accession = cursor.fetchall()
    # print all_accession
    all_accession = [list(a) for a in all_accession]
    all_accession = [[str(a[i]) for i, var_i in enumerate(a)] for a in all_accession]
    cik_accession_0603 = ['_'.join(a) for a in all_accession]
    print len(set(cik_accession_0603))
    # diff_step1_step3 = list(set(all_filing) - set(cik_accession_0601))
    # diff_step1_step2 = list(set(all_filing) - set(exec_comp_tables_final))
    diff_step2_step3 = list(set(exec_comp_tables_final) - set(cik_accession_0603))
    # print ("Number of ciks/accession in TABLES_DATEs but not in bill_exec_0602: " + str(len(diff_step1_step3)))
    # print ("Number of ciks/accession in TABLES_DATEs but not in exec_comp_tables_final "+str(len(diff_step1_step2)))
    print ("Number of ciks/accession in exec_comp_tables_final but not in bill_exec_0606 "+str(len(diff_step2_step3)))



    # with open(txtpath + 'diff_step1_step3.txt', 'w') as df:
    #     # df.write("IN TABLES DATE but not in bill_exec_0601 \n")
    #     for element in diff_step1_step3:
    #         df.write(element + '\n')

    # with open(txtpath + 'diff_step1_step2.txt', 'w') as df:
    #     # df.write("IN TABLES DATE but not in bill_exec_0601 \n")
    #     for element in diff_step1_step2:
    #         df.write(element + '\n')

    with open(txtpath + 'diff_step2_step3_0606.txt', 'w') as df:
        # df.write("IN exec_comp_tables_final but not in bill_exec_0601 \n")
        for element in diff_step2_step3:
            df.write(element + '\n')

    db.close()


# sql = '''CREATE TABLE IF NOT EXISTS bill_exec_addition(
#                         id BIGINT NOT NULL AUTO_INCREMENT,
#                         name TEXT,
#                         title TEXT,
#                         year INT(11),
#                         salary DECIMAL(11,2),
#                         bonus DECIMAL(11,2),
#                         stock_awards DECIMAL(11,2),
#                         option_awards DECIMAL(11,2),
#                         RSUs DECIMAL(11,2),
#                         nonequity_incentive_plan_compensation DECIMAL(11,2),
#                         change_in_pension_value_and_nonqualified_deferred_compensation DECIMAL(11,2),
#                         securities_underlying_options DECIMAL(11,2),
#                         all_other DECIMAL(11,2),
#                         total DECIMAL(11,2),
#                         remainder DECIMAL(11,2),
#                         accession VARCHAR(255),
#                         cik INT(11),
#                         file_date DATE,
#                         KEY(id)
#               ) SELECT B.* FROM (SELECT * FROM bill_exec_0531) AS B LEFT OUTER  JOIN (SELECT * FROM
#     bill_exec) AS A ON B.accession = A.accession WHERE A.accession IS NULL'''
