#!/usr/bin/python
import MySQLdb
from collections import defaultdict, Counter
import multiprocessing
import re
import jellyfish as js
from nltk import word_tokenize

# """
# For each company cik in the table, pull all the individual names and ciks from the reporters_345 table (form_345)
# Use Levenshtein Distance to compare the last names from reporters_345 with all names from the exec comp.
# **Since the 345 data is more structured, we can be fairly certain that we know the LAST name for each officer,
# while the names
# extracted from exec comp have more variation in order and completeness.
# After each of the individual ciks is assigned and inserted into the db, join on the individuals table to get the
# individual ids associated
# with each individual cik.
# """

exec_comp_table = "bill_exec_0720"

def get_proxy_ciks():
    db = MySQLdb.connect("localhost", "root", "Edgar20!4", "def14a")
    cursor = db.cursor()
    cursor.execute("select distinct(cik) from %s where ind_cik is null" % exec_comp_table)
    all_ciks = cursor.fetchall()
    cik_list = [a[0] for a in all_ciks]
    db.close()
    cik_list.reverse()
    return cik_list


def name_pre_process(name_string):
    regex = re.compile('[^a-zA-Z]')
    name = regex.sub(' ', name_string)
    repls = {'former' : ' ', 'president' : ' ', 'vice':' ', 'chief':' ', 'executive':' ', 'officer':' ', 'and':' '}
    name = reduce(lambda a, kv: a.replace(*kv), repls.iteritems(), name).strip()
    return name


def get_name_tokens(name_string):
    name = unicode(name_string, "utf-8").replace('.', '').lower()
    tokens = word_tokenize(name)
    return tokens


def preprocess_two(officer_name):
    #o'sullivan case
    for n in officer_name:
        if n == 'o' or n == 'd':
            idx = officer_name.index(n) + 1
            try:
                new_name = n + officer_name[idx]
                officer_name.append(new_name)
            except IndexError:
                pass
    return officer_name


def get_reporters_dict(cik):
    reporters_dict = defaultdict(list)

    db = MySQLdb.connect("localhost", "root", "Edgar20!4", "form_345")
    cursor = db.cursor()
    cursor.execute("select distinct owner_cik, owner_name, filing_date from reporters_345 where issuer_cik = %i" % cik)
    data = cursor.fetchall()
    db.close()

    for d in data:

        full_name = get_name_tokens(d[1])
        #for O'Sullivan case:
        if len(full_name[0]) == 1:
            full_name[0:2] = [''.join(full_name[0:2])]

        last_name = full_name[0]

        reporters_dict[d[2]].append((d[0], full_name[1:], last_name))

    return reporters_dict


def check_last_name(last_names, officer_name):
    poss_match = []
    for l in last_names:
        for o in officer_name:
            if js.damerau_levenshtein_distance(l[0], o) == 0:
                poss_match.append(l)
    return poss_match


def check_other_names(officer_name, poss_names):
    poss_match_dict = Counter()
    for p in poss_names:
        for n in p[0]:
            for o in officer_name:
                if js.damerau_levenshtein_distance(n, o) == 0:
                    poss_match_dict[p[1]] += 1

    return poss_match_dict


def update_table(id, cik):

    update_db = MySQLdb.connect("localhost", "root", "Edgar20!4", "def14a")
    update_cursor = update_db.cursor()

    try:
        update_cursor.execute("update %s set ind_cik = %i where id = %i" % (exec_comp_table, cik, id))
        update_db.commit()

    except MySQLdb.Error as e:
        update_db.rollback()
        print e
    update_cursor.close()


def handle_proxy_cik((cik)):
    # print (cik)
    textfile.write("====================================== Proxy CIK:  %i \n" % cik)

    rep_dict = get_reporters_dict(cik)

    last_names = list(set((n[2], n[0]) for y in rep_dict.values() for n in y))
    first_middle_names = list(set((tuple(n[1]), n[0]) for y in rep_dict.values() for n in y))

    cursor = db.cursor()

    cursor.execute("select id, name, title, file_date from %s where cik = %i and ind_cik is null" % (exec_comp_table, cik))
    data = cursor.fetchall()
    cursor.close()

    for d in data:
        print str(d) + " out of " + str(len(data))
        if d[1]:

            officer_name = get_name_tokens(name_pre_process(d[1]))
            title = get_name_tokens(name_pre_process(d[2]))
            all_names = officer_name + title
            officer_name = preprocess_two(all_names)
            textfile.write("Officer Name: %s  \n" % officer_name)
            print "officer name", officer_name

            first_pass = check_last_name(last_names, officer_name)

            if first_pass:
                if len(first_pass) == 1:
                    cik = first_pass[0][1]
                    update_table(d[0], cik)
                    #print "execute:", d[0]
                    textfile.write("Match on first pass \n")

                else:
                    if len(set(i[1] for i in first_pass)) == 1:
                        update_table(d[0], cik)
                        #print "execute:", d[0]
                        textfile.write("Match all ciks were the same \n")
                    else:
                        textfile.write("Need *Second* Pass: %s  \n" % str(first_pass))
                        poss_ciks = [i[1] for i in first_pass]
                        poss_other_names = [n for n in first_middle_names if n[1] in poss_ciks]
                        second_pass = check_other_names(officer_name, poss_other_names)
                        if second_pass:
                            if len(second_pass) > 1:
                                #check to see if there is a unique max, if there is, pick it
                                high = second_pass.most_common(2)
                                if high[0][1] == high[1][1]:
                                    textfile.write("NO match on *Second* Pass: %s  \n" % str(second_pass))
                                else:
                                    cik = high[0][0]
                                    update_table(d[0], cik)
                                    textfile.write("Match on second pass \n")
                            else:
                                cik = second_pass.keys()[0]
                                update_table(d[0], cik)
                                textfile.write("Match on second pass \n")
                        else:
                            textfile.write("second pass length == 0 \n")

            else:
                print "no match", officer_name
        else:
            textfile.write("No name in name field \n")

    textfile.write("=============================\n")

    return None


def mp_handler():

    global db
    db = MySQLdb.connect("localhost", "root", "Edgar20!4", "def14a")
    p = multiprocessing.Pool(2)
    p.map(handle_proxy_cik, proxy_ciks)
    db.close()

if __name__ == '__main__':

    with open('proxy_name_0720.txt', 'w') as textfile:

        textfile.write("Proxy Name Matching \n")
        textfile.write("=========================== \n")

        proxy_ciks = get_proxy_ciks()

        print "Num ciks:", len(proxy_ciks)
        mp_handler()

    print "done"
