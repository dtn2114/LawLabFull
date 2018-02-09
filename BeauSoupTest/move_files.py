#!/usr/bin/python
import shutil
import glob
import os
# path = '/local/bill_test/'
srcpath = '/local/def14a_extract/tables_dates/'
# path = '/local/def14a_extract/exec_comp_tables_final'
dstpath = '/local/def14a_extract/tables_pass_two/'

# with open('diff_step1_step2.txt', 'r') as df:
#     i = 0
#     for line in df:
#         # print line
#         cik_accession = line
#         cik = cik_accession.split('_')[0]
#         accession = cik_accession.split('_')[1].rstrip()
#         src = srcpath + cik + '/' + accession +'_'+'*[0-9].txt'
#         # i+=1
#         for filename in glob.glob(src):
#             dst = dstpath+ cik + '_'+ os.path.basename(filename)
#             print dst
#             try:
#                 shutil.copyfile(filename, dst)
#             except Exception, e:
#                 i+=1
#                 print "Failed %s %s" %(filename,e)
# print i

##Copy things from exec_comp_tables_final to tables_pass_three
# srcpath = '/local/def14a_extract/exec_comp_tables_final/'
# # path = '/local/def14a_extract/exec_comp_tables_final'
# dstpath = '/local/def14a_extract/tables_pass_three_test/'
#
# with open('diff_step2_step3.txt', 'r') as ef:
#     for line in ef:
#         cik_accession = line
#         cik = cik_accession.split('_')[0]
#         accession = cik_accession.split('_')[1].rstrip()
#         src = srcpath + accession + '_' + cik + '_' +'*[0-9].txt'
#         for filename in glob.glob(src):
#             dst = dstpath+ os.path.basename(filename)
#             # print dst
#             try:
#                 shutil.copyfile(filename, dst)
#             except Exception,e:
#                 print "Failed %s %s" %(filename,e)
#             # print dst

#copy things from table_pass_three to tables_pass_three_0603
# srcpath = '/local/def14a_extract/tables_pass_three/'
srcpath = '/local/bill_test/exec_comp_tables_final/'
dstpath = '/local/def14a_extract/tables_pass_three_0604/' #what in exec

with open('diff_step2_step3_0603.txt', 'r') as ef:
    for line in ef:
        cik_accession = line
        cik = cik_accession.split('_')[0]
        accession = cik_accession.split('_')[1].rstrip()
        src = srcpath + accession + '_' + cik + '_' +'*[0-9].txt'
        for filename in glob.glob(src):
            dst = dstpath+ os.path.basename(filename)
            # print dst
            try:
                shutil.copyfile(filename, dst)
            except Exception,e:
                print "Failed %s %s" %(filename,e)
            # print dst




# 0000023194-07-000025_23194_1
# TESTING
# path = '/Users/bill/PycharmProjects/BeauSoupTest/textfiles/table_dates/'
# cik = '1206264'
# accession = '0001140361-14-014415'#_20140327'
# src = path + cik + '/'+ accession + '_' + '*.txt'
# # print src
# for filename in glob.glob(src):
#     print filename
#     dst = '/Users/bill/PycharmProjects/BeauSoupTest/textfiles/'
#     shutil.copy(filename, dst)