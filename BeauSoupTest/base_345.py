#!/usr/bin/python
import xml.dom
import traceback
from extraction import *
import xml.etree.ElementTree as ET
import urllib2
import re
import os
from os import path
import MySQLdb
import base_sql

def get_text(text_file):
    with open(text_file) as f:
        data = f.read().replace('\n', '')
    return data


def get_xml(filing_name):

    page_raw_text = get_text(filing_name)

    date_start = 'FILED AS OF DATE'
    s = [m.start() for m in re.finditer(date_start, page_raw_text)]
    date = page_raw_text[s[0]:s[0]+len(date_start)+15].strip()
    filing_date = re.sub('[^0-9]','', date)

    xml_start = '<XML>'
    xml_end = '</XML>'

    xml_docs_start = [m.start() for m in re.finditer(xml_start, page_raw_text)]
    xml_docs_end = [m.start() for m in re.finditer(xml_end, page_raw_text)]

    doc_start = xml_docs_start[0] + len(xml_start)
    doc_end = xml_docs_end[0]
    doc = page_raw_text[doc_start:doc_end].strip()

    redun_end = [m.start() for m in re.finditer(">", doc)]
    doc = doc[redun_end[0]+1:]

    clean_doc = re.sub('&', '&amp;', doc)

    root = ET.fromstring(clean_doc)

    return filing_date, root


if __name__ == '__main__':

	##########################################
	# CREATE THE PREPROCESSED UPDATED TABLE, DROP OLD UPDATE TABLE IF EXISTS
	##########################################
    base_sql.create_tables() 
   	
   	##########################################
	# EXTRACT INFO OUT OF FORM_345 TO INSERT INTO THE 5 STANDARD TABLES
	##########################################
    issuers_query = "INSERT INTO filers_345_update(`accession`, `filer_cik`, `filing_date`, `form_type`, `no_securities_owned`, `issuer_cik`, `issuer_name`, `ticker`, `num_reporters`, `num_non_derivatives`, `num_derivatives`, `exit_box`, `is_amendment`)" \
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    reporters_query = "INSERT INTO reporters_345_update(`accession`,`filer_cik`, `filing_date`, `form_type`, `issuer_cik`, `owner_cik`, `owner_name`, `owner_street1`, `owner_street2`, `owner_city`, `owner_state`, `owner_zip`, `is_director`, `is_officer`, `is_ten_percent`, `is_other`, `officer_title`, `other_text`, `reporter_count`, `issuer_id`)" \
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    non_der_query = "INSERT INTO non_derivative_update(`accession`,`filer_cik`, `filing_date`, `issuer_cik`, `form_type`, `title`, `title_foot`, `transaction_date`, `transaction_date_foot`, `deemed_execution_date`, `deemed_foot`, `transaction_form`, `transaction_code`, `equity_swap`, `transaction_coding_foot`, `timeliness`, `timeliness_foot`, `transaction_shares`, `transaction_foot`, `transaction_price`, `price_foot`, `transaction_acquired_code`, `acquired_foot`, `shares_owned`, `shares_owned_foot`, `ownership`, `ownership_foot`, `nature`, `nature_foot`, `d_count`, `issuer_id`)"\
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    der_query = "INSERT INTO derivative_update(`accession`,`filer_cik`, `filing_date`, `issuer_cik`, `form_type`, `title`, `title_foot`, `exercise_price`, `exercise_foot`, `exercise_date`, `exercise_date_foot`, `transaction_date`, `transaction_date_foot`, `deemed_execution_date` ,`deemed_foot`, `transaction_form`, `transaction_code`, `equity_swap`, `transaction_coding_foot`, `timeliness`, `timeliness_foot`, `transaction_shares`, `shares_foot`, `transaction_price`, `price_foot`, `transaction_acquired_code`, `acquired_foot`, `expire_date`, `expire_foot`, `underlying_security`, `security_foot`, `underlying_shares`, `underlying_shares_foot`, `shares_following_transaction`, `shares_following_foot`, `ownership`, `ownership_foot`, `nature`, `nature_foot`, `d_count`, `issuer_id`)"\
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    sec_query = "INSERT INTO filer_securities_update(`accession`, `filer_cik`, `filing_date`, `form_type`, `issuer_cik`, `issuer_name`, `ticker`, `owner_cik`, `owner_name`, `is_director`, `is_officer`, `is_ten_percent`, `is_other`, `officer_title`, `other_text`, `total_securities`, `issuer_id`, `exit_box`)" \
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    db = MySQLdb.connect("localhost", "root", "Edgar20!4", "bill")
    cursor = db.cursor()

    forms_dir = ['/form4/edgar/data/', '/form3/edgar/data/', '/form4_amend/edgar/data/', '/form5/edgar/data/']

    for i in range(len(forms_dir)):
        present_directory = os.getcwd() + forms_dir[i]
        with open('errors.txt', 'w') as textfile:
            error_count = 1
            count = 1
            for directory in os.listdir(present_directory):
                # print "count", count
                count += 1
                filer_cik = directory.strip()
                # print "cik", filer_cik
                #next_dir = os.path.join(present_directory, directory)
                next_dir = present_directory + '%s/' % filer_cik
                if os.path.isdir(next_dir):
                    for filing in os.listdir(next_dir):
                        #for filing in os.listdir(present_directory):
                        accession = filing.rstrip('.txt').strip()
                        filing_location = next_dir + '%s' % filing
                        #filing_location = present_directory + '%s' % filing
                        try:
                            filing_date = get_xml(filing_location)[0]
                            last_row_id = None
                            insert_list = [accession, filer_cik, filing_date]
                            root = get_xml(filing_location)[1]
                            try:
                                data = extract_form(root)
                                if data[0]:
                                    insert_list.extend(data[0])
                                    try:
                                        cursor.execute(issuers_query, tuple(insert_list))
                                        last_row_id = cursor.lastrowid
                                        db.commit()
                                        for l in data[1]:
                                            try:
                                                rlist = [accession, filer_cik, filing_date]
                                                rlist.extend(l)
                                                rlist.append(last_row_id)
                                                cursor.execute(reporters_query, tuple(rlist))
                                                db.commit()
                                            except MySQLdb.Error as e:
                                                db.rollback()
                                                # print e
                                                textfile.write(str(error_count) +"reporter_insert " + filing_location+ "\n")
                                                error_count += 1
                                        if data[2]:
                                            for d in data[2]:
                                                try:
                                                    dlist = [accession, filer_cik, filing_date]
                                                    dlist.extend(d)
                                                    #dlist[-1] = str(dlist[-1]) + '-' + accession + filer_cik
                                                    dlist.append(last_row_id)
                                                    cursor.execute(non_der_query, tuple(dlist))
                                                    db.commit()
                                                except MySQLdb.Error as e:
                                                    db.rollback()
                                                    # print e
                                                    textfile.write(str(error_count) + "non_derivatives_insert " + filing_location + "\n")
                                                    error_count += 1
                                        if data[3]:
                                            for d in data[3]:
                                                try:
                                                    dlist = [accession, filer_cik, filing_date]
                                                    dlist.extend(d)
                                                    #dlist[-1] = str(dlist[-1]) + '-' + accession + filer_cik
                                                    dlist.append(last_row_id)
                                                    #print dlist
                                                    dlist = [i.encode('ascii','ignore') for i in dlist]
                                                    cursor.execute(der_query, tuple(dlist))
                                                    db.commit()
                                                except MySQLdb.Error as e:
                                                    db.rollback()
                                                    # print e
                                                    textfile.write(str(error_count) + "derivatives_insert " + filing_location + "\n")
                                                    error_count += 1
                                        sec_list = insert_list[0:4] + insert_list[5:8] + data[4][2:4] + data[4][9:15]
                                        sec_list.append(data[5])
                                        sec_list.append(last_row_id)
                                        sec_list.append(insert_list[-2])
                                        try:
                                            cursor.execute(sec_query, sec_list)
                                        except MySQLdb.Error as e:
                                            db.rollback()
                                            # print e
                                            textfile.write(str(error_count) + "sec_list not updated" + filing_location + "\n")
                                            error_count += 1
                                    except MySQLdb.Error as e:
                                        db.rollback()
                                        # print e
                                        textfile.write(str(error_count) + "filer_insert " + filing_location + "\n")
                                        error_count += 1
                                else:
                                    textfile.write(str(error_count) + "no data " + filing_location + "\n")
                                    error_count += 1

                            except xml.etree.ElementTree.ParseError as e:
                                textfile.write(str(error_count) + "parse error  " + str(e) + filing_location + "\n")
                                textfile.write(' '.join(traceback.format_exc().splitlines()))
                                error_count += 1
                                pass
                                # print "can't extract"
                            except urllib2.URLError as e:
                                textfile.write(str(error_count) + "urllib error " + str(e) + filing_location + "\n")
                                textfile.write(' '.join(traceback.format_exc().splitlines()))
                                error_count += 1
                                pass
                                # print "can't extract"
                            except IndexError as e:
                                textfile.write(str(error_count) + "Index error  " + str(e) + filing_location + "\n")
                                textfile.write(' '.join(traceback.format_exc().splitlines()))
                                error_count += 1
                                pass
                                # print "can't extract"
                            except KeyError as e:
                                textfile.write(str(error_count) + "damn Keyerror  " + str(e) + filing_location + "\n")
                                textfile.write(' '.join(traceback.format_exc().splitlines()))
                                error_count += 1
                                pass
                                # print "can't extract"
                            except AttributeError as e:
                                textfile.write(str(error_count) + "Attribute Error " + str(e) + filing_location + "\n")
                                textfile.write(' '.join(traceback.format_exc().splitlines()))
                                error_count += 1
                                pass
                                # print "can't extract"
                                # except:
                                #     textfile.write("Other Error " + filing_location + "\n")
                                #     pass
                        except IndexError as e:
                            textfile.write(str(error_count) + "Index error  " + str(e) + filing_location + "\n")
                            textfile.write(' '.join(traceback.format_exc().splitlines()))
                            error_count += 1
                            pass
                            print "nope"
                        except IOError as e:
                            textfile.write(str(error_count) + "IO error  " + str(e) + filing_location + "\n")
                            textfile.write(' '.join(traceback.format_exc().splitlines())+ "\n")
                            error_count += 1
                            pass
                            print "nope"
                        except xml.etree.ElementTree.ParseError as e:
                            textfile.write(str(error_count) + "parse error  " + str(e) + filing_location + "\n")
                            textfile.write(' '.join(traceback.format_exc().splitlines()))
                            error_count += 1
                            pass
                            print "nope"
                else:
                    print "not a directory"
                    textfile.write("not a dir  \n")
        print "Done " + forms_dir[i]
    print "Done"

    db.close()
