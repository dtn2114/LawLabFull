#!/usr/bin/python

from bs4 import *
import urllib2
import types
import requests
import re
import csv
import glob
import string
from collections import defaultdict
from decimal import *
import os
import locale
import MySQLdb
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

#FUNCTIONS
def adjust_col_strings(raw, rowspan):
    col_strings = []
    for st in raw:
        processed = st.replace(u'\u2014', '0').replace(u'\x97', '0').replace(u'\uFE58', '0').encode('ascii', 'replace').replace('?', ' ').replace('\n', ' ')
        if processed.strip():
            col_strings.append(processed)
    if len(col_strings) > rowspan:
        col_strings[rowspan - 1] = ' '.join(col_strings[rowspan - 1:])
    else:
        for i in range(len(col_strings), rowspan):
            col_strings.append('')
    return col_strings

def balance_rows(data, num_col):
    for i, row in enumerate(data):
        diff = num_col - len(row)
        if diff:
            row = row + [''] * diff
        data[i] = row
    return data

def clean_data(data):
    data = remove_whitespace(data)
    data = remove_footnote(data)
    data = remove_dollar(data)
    data = remove_empty_data_cols(data)
    return data

def classify_rows(data):
    for i, row in enumerate(data):
        if is_data_row(row):
            #print (row)
            return i - 1

def combine_headers(data, header_ind):
    #print(header_ind)
    if header_ind == -1:
        return [list(a) for a in data]
    if 'year' in data[header_ind+1][1].lower():
        header_ind += 1
    headers = data[0:header_ind + 1]
    zipped = zip(*headers)
    combined = [[' '.join(a) for a in zipped]]
    combined.extend(data[header_ind+1:])
    return [list(a) for a in combined]

def create_titles(data):
    orig_year = get_orig_year(data)
    if '-' in orig_year:
        orig_year = orig_year.split('-')[0]
    else:
        orig_year = orig_year
    #titles = []
    title = []
    count = 1
    name = ''
    for i, row in enumerate(data):
        #print row
        if 'year' in row[1].lower():
            data[i].append('Title')
        else:
            #if "|" in row[0]:
            if row[1].split('-')[0] != orig_year and 'year' not in row[1].lower() and 'name' not in row[0].lower():
                if i+1 == len(data):
                    entries = row[0].split("|")
                    e = next((k for k, j in enumerate(entries) if j.strip()), 0)
                    entry = entries[e:]
                    title.append(' '.join(entry))
                    data[i][0] = name
                    for k in range(count, len(data)):
                        if data[k][1].isdigit():
                            data[k].append(' '.join(title))
                else:
                    entries = row[0].split("|")
                    e = next((k for k, j in enumerate(entries) if j.strip()), 0)
                    entry = entries[e:]
                    title.append(' '.join(entry))
                    data[i][0] = name
            else:
                if i != 1:
                    if i+1 == len(data):
                        for j in range(count, i):
                            if data[j][1].isdigit():
                                data[j].append(' '.join(title))
                        entries = row[0].split('|')
                        e = next((k for k, j in enumerate(entries) if j.strip()), 0)
                        entry = entries[e+1:]
                        data[i].append(' '.join(entry))
                        data[i][0] = entries[e]
                    else:
                        #print title
                        for j in range(count, i):
                            if data[j][1].isdigit():
                                data[j].append(' '.join(title))
                        title =[]
                        entries = row[0].split("|")
                        e = next((k for k, j in enumerate(entries) if j.strip()), 0)
                        entry = entries[e+1:]
                        title.append(' '.join(entry))
                        name = entries[e]
                        count = i
                else:
                    entries = row[0].split("|")
                    e = next((k for k, j in enumerate(entries) if j.strip()), 0)
                    entry = entries[e+1:]
                    title.append(' '.join(entry))
                    #print title
                    name = entries[e]
                    count = i

def csvToArray(filePath):
    readFile = open(filePath, 'r+')
    reader = csv.reader(readFile)
    array = []
    for row in reader:
        array.append(row)
    readFile.close()
    return array

def decimal_dollar(row):
    for i in range(len(row)):
        row[i]=row[i].replace(',','')
        #print(i,type(i),is_number(i))
        if is_number(row[i]):
            row[i]=Decimal(row[i])
            #print(i,type(i))
    #print(row[7],type(row[7]))
    return row

def get_name(data):
    for i, row in enumerate(data):
        if 'year' in row[1].lower():
            [re.sub(u'\|', '', cell) for cell in row]
        else:
            if "|" in row[0]:
                entries = row[0].split("|")
                exist = next(k for k, j in enumerate(entries) if j.strip())
                data[i][0] = entries[exist]
            if "," in row[0]:
                entries = row[0].strip().split(',')
                #print(row[0])
                empty = next((k for k,j in enumerate(entries)if not j.strip()), len(entries))
                data[i][0] = ''.join(entries[:empty])
    return remove_slash(data)

def get_lines_with(data, keywords):
        lines = []
        # combine two rows if they are for the same exhibit number
        for row in data:
            if row[0]:  # there is a exhibit number
                lines.append(' '.join(row))
            else:
                if lines:
                    lines.append(lines.pop() + ' ' + ' '.join(row))
                else:
                    lines.append(' '.join(row))
        rows = lines
        lines = []
        # split one line into two if there is a separator, ;
        for row in rows:
            if ";" in row:
                entries = row.split(";")
                for entry in entries:
                    lines.append(entry)
            else:
                lines.append(row)
        rows = lines
        lines = []
        for row in rows:
            if any(keyword.lower() in row.lower() for keyword in keywords):
                lines.append(row.strip())
        return lines

def get_orig_year(data):
    for i, row in enumerate(data):
        if is_data_row(row):
            return row[1]

def getFullness(row):
    fullness = 0
    for val in row:
        if val:
            fullness += 1
    return fullness

def is_data_row(row):
    #joined = ''.join(row[1:])
    row = [cell.strip() for cell in row]
    row = filter(bool, row)
    #print row
    for cell in row[1:]:
        if percent_digit_or_dash(cell.split()[0]) > 0.9:
            return True
    return False

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def percent_digit_or_dash(st):
    stLen = len(st)
    #print(st)
    if stLen == 0:
        return 0.0
    numDigits = sum([1 for x in st if x.isdigit() or x == '-' or x == '$' or x == '%' or x == '.' or x ==
                     ','])

    percent = float(numDigits)/float(stLen)
    return percent

def remove_whitespace(data):
    data = [[re.sub(u'^\s*', '', cell) for cell in row] for row in data]  # remove from the start
    data = [[re.sub(u'\s*$', '', cell) for cell in row] for row in data]  # remove from the end
    return [[re.sub(u'\s+', ' ', cell) for cell in row] for row in data]  # remove from the middle

def remove_footnote(data):
    #remove things like (1), (2) footnotes
    return [[re.sub(u'\(\d*\)', '', cell) for cell in row] for row in data]

def remove_dollar(data):
    #remove dollar sign, hash sign.
    return [[re.sub(u'\(\$*\)|\(\#*\)|\$*', '', cell) for cell in row] for row in data]

def remove_empty_row(data):
    lst = []
    for i, row in enumerate(data):
        if not is_data_row(row) and 'year' not in row[1].lower():
            lst.append(i)
        else:
            pass
    lst = set(lst)
    return [v for i, v in enumerate(data) if i not in lst]

def remove_slash(data):
    return [[re.sub(u'\|', '', cell) for cell in row] for row in data]

def remove_empty_cols_rows(data, keepSparse = True, duplicates = []):
    rows = None
    cols = None
    if duplicates:
        modify_duplicates = True
    else:
        modify_duplicates = False
    if modify_duplicates:
        rows = [i for i, row in enumerate(data) if not (any(row))]
    data = [list(row) for row in data if any(row)]
    data = zip(*data)
    if keepSparse:
        if modify_duplicates:
            cols = [i for i, row in enumerate(data) if not (any(row))]
        data = [list(row) for row in data if any(row)]
    else:
        if modify_duplicates:
            cols = [i for i, row in enumerate(data) if not (getFullness(row) > 2)]
        data = [list(row) for row in data if (getFullness(row) > 2)]
    data = zip(*data)
    data = [list(row) for row in data]
    if modify_duplicates:
        new_duplicates = []
        for duplicate in duplicates:
            new_duplicate = []
            for point in duplicate:
                if point[0] not in rows and point[1] not in cols:
                    new_point = point
                    rowShift = 0
                    for row in rows:
                        if row < new_point[0]:
                            rowShift += 1
                    new_point[0] = new_point[0] - rowShift
                    colShift = 0
                    for col in cols:
                        if col < new_point[1]:
                            colShift += 1
                    new_point[1] = new_point[1] - colShift
                    new_duplicate.append(new_point)
            if new_duplicate:
                new_duplicates.append(new_duplicate)
        return (data, new_duplicates)
    return (data, None)

def remove_empty_data_cols(data):
    #data = [[cell for cell in row if any(cell)] for row in data]
    #print data
    data = zip(*data)
    #print data
    data = [[cell.strip() for cell in row] for row in data]
    data = [list(row) for row in data if any(row[1:])]
    data = zip(*data)
    data = [list(row) for row in data]
    return data

def remove_horizontal_header_duplicates(duplicates, data, header_ind):
    if duplicates is None:
        return data
    cols_to_delete = []
    for duplicate in duplicates:
        last_row = duplicate[0][0]
        cols = []
        for point in duplicate:
            col = point[1]
            row = point[0]
            if col not in cols:
                cols.append(col)
            if row > last_row:
                last_row = row
        if header_ind == last_row and len(cols) > 1:
            first_col = min(cols)
            ############# merge rows, delete those with no headers
            for col in cols:
                if not col == first_col:
                    cols_to_delete.append(col)
            lenData = len(data)
            for i in range(0, lenData):
                if i > last_row:
                    row = data[i]
                    colStr = ''
                    for col in cols:
                        colStr = colStr + row[col]
                    rowList = list(row)
                    rowList[first_col] = colStr
                    rowTuple = tuple(rowList)
                    data[i] = rowTuple
    data = zip(*data)
    # for ind, col in enumerate(data):
    #     if not col[header_ind]:
    #         cols_to_delete.append(ind)
    sorted_cols = sorted(unique(cols_to_delete))
    sorted_cols.reverse()
    for col in sorted_cols:
        data.pop(col)
    data = zip(*data)
    return data

def replace_tag(elem):
    soup=elem
    if soup.br is not None:
        soup = str(soup)
        soup = re.sub(r"</?br?>", "|", soup)
        soup = BeautifulSoup(soup)
        return soup
    elif len(soup.find_all('p', text=True))>1:
        for tag in soup.find_all('p', text=True):
            text = tag.string
            tag.string.replace_with(text+'|')
        return soup
    elif len(soup.find_all('div', text=True))>1:
        for tag in soup.find_all('div', text=True):
            text = tag.string
            tag.string.replace_with(text+'|')
        return soup
    else:
        return soup

def split_line(data):
    #Split one line into two if year column has more than 1 year
    orig_year = get_orig_year(data)
    if '-' in orig_year:
        orig_year = orig_year.split('-')
    else:
        orig_year = orig_year.split()
    if len(orig_year) > 1:
        lines = []
        for i, row in enumerate(data):
            if is_data_row(row):
                for j in range(1, len(row)):
                    row[j] = row[j].split()
                line = row[1:]
                line = zip(*line)
                for k, entry in enumerate(line):
                    if entry[0].strip().split('-')[0] == orig_year[0]:
                        line[k] = (row[0], ) + entry
                        line[k] = list(line[k])
                        lines.append(line[k])
                    else:
                        line[k] = ('', ) + entry
                        line[k] = list(line[k])
                        lines.append(line[k])
            else:
                lines.append(row)
        return lines
    else:
        return data

def unique(seq):
   # not order preserving
   set = {}
   map(set.__setitem__, seq, [])
   return set.keys()

def writeToCSV(matrix, filePath, type):
    thisFile = open(filePath, type)
    writer = csv.writer(thisFile)
    for row in matrix:
        writer.writerow(row)
    thisFile.close()

def write_super_headers(duplicates, data, header_ind):
    #print(duplicates)
    if duplicates is None:
        return data
    for duplicate in duplicates:
        last_row = duplicate[0][0]
        first_row = duplicate[0][0]
        cols = []
        for point in duplicate:
            col = point[1]
            row = point[0]
            if col not in cols:
                cols.append(col)
            if row > last_row:
                last_row = row
        if header_ind > last_row and len(cols) > 1:
            super_header_text = data[duplicate[0][0]][duplicate[0][1]]
            #print(duplicate)
            for point in duplicate:
                if point[0] == first_row:
                    data[point[0]][point[1]] = super_header_text
    return data

def get_table(filename):
    data = open(filename).read()
    soup = BeautifulSoup(data)
    found_key = soup.find(text = re.compile('\s*Summary\s*',re.IGNORECASE))
    if found_key!=None:
        if found_key.find_parent('table') != None:
            table = found_key.find_parent('table')
        else:
            table = found_key.find_next('table') #find the next table using the table_key
    else:
        table = soup.find('table')

    # balance table using colspan, rowspan
    result = defaultdict(lambda: defaultdict(unicode))
    duplicates = []
    # try:
    for row_i, row in enumerate(table.find_all('tr')):
        for col_i, col in enumerate(row.find_all(['td', 'th'])):
            if col_i == 0:
                col = replace_tag(col)
            colspan = int(col.get('colspan', 1))
            rowspan = int(col.get('rowspan', 1))
            while row_i in result and col_i in result[row_i]:
                col_i += 1
            is_duplicate = False
            if rowspan > 1 or colspan > 1:
                duplicate = []
                is_duplicate = True
            col_strings = adjust_col_strings(col.strings, rowspan)
            for i in range(row_i, row_i + rowspan):
                for j in range(col_i, col_i + colspan):
                    if j == col_i:
                        result[i][j] = col_strings[i - row_i]
                    else:
                        result[i][j] = ''
                    if is_duplicate:
                        duplicate.append([i, j])
            if is_duplicate:
                duplicates.append(duplicate)

    data = []
    num_col = 0
    for i, row in sorted(result.items()):
        cols = []
        for j, col in sorted(row.items()):
            cols.append(col.strip())
        if len(cols) > num_col:
            num_col = len(cols)
        data.append(cols)
    #print data
    data = balance_rows(data, num_col)
    data, duplicates = remove_empty_cols_rows(data, duplicates = duplicates)
    header_ind = classify_rows(data)
    print header_ind
    if header_ind is not None:
        data = write_super_headers(duplicates, data, header_ind)
        data = remove_horizontal_header_duplicates(duplicates, data, header_ind)
        data = combine_headers(data, header_ind)
    data = clean_data(data)
    data = split_line(data)
    create_titles(data)
    data = get_name(data)
    data = remove_empty_row(data)
    #writeToCSV(data, csvfile, writetype)
    return data

def match_header_dict(data_headers, filename):
    headers_dict = {'name': [], 'year': [], 'title': [], 'salary': [], 'bonus': [], 'stock': [], 'option': [],
                    'total': [],
                    'restricted': [], 'incentive': [], 'pension': [], 'other': [], 'securities': [], 'remainders': []}
    total_headers = len(data_headers)
    headers_found = []
    for index, (header_i, i) in enumerate(headers_dict.items()):
        for j, header_j in enumerate(data_headers):
            if header_i in header_j.lower():
                headers_dict[header_i].append(j)
                headers_found.append(j)
    with open('remainder.txt', 'a') as textFile:
        textFile.write(filename + "\n")
        for i in range(0, total_headers):
            if i not in headers_found:
                headers_dict['remainders'].append(i)
                textFile.write("\t" + data_headers[i]+"\n")
    return headers_dict

def rearrange_data(data, filename):
    table = []
    fixed_header = ['name', 'year', 'title', 'salary', 'bonus', 'stock', 'option',
                    'restricted', 'incentive', 'pension', 'other', 'securities', 'remainders', 'total']
    table.append(fixed_header)
    headers_dict = match_header_dict(data[0], filename)
    for j, row in enumerate(data[1:]):
        line = []
        for e, header_e in enumerate(table[0][:3]):
            cell_lst = headers_dict[header_e]
            if not cell_lst:
                value = ''
            else:
                if len(cell_lst) > 1:
                    raise Exception
                else:
                    value = row[cell_lst[0]]
            line.append(value.strip())
        for i, header_i in enumerate(table[0][3:len(table[0])]):
            cell_lst = headers_dict[header_i]
            value = Decimal(0)
            if not cell_lst:
                value = value
            else:
                if len(cell_lst) > 1:
                    for k in cell_lst:
                        amount = row[k].strip('-')
                        amount = ''.join([a.strip() for a in amount.split(',')])
                        value = value + (Decimal(locale.atoi(amount)) if amount else Decimal(0))
                else:
                    amount = row[cell_lst[0]].strip('-')
                    amount = ''.join([a.strip() for a in amount.split(',')])
                    value = Decimal(locale.atoi(amount)) if amount else Decimal(0)
            line.append(value)
        table.append(line)
    return table

if __name__ == '__main__':
    # db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "def14a")
    # cursor = db.cursor()
    #
    # sql = '''CREATE TABLE IF NOT EXISTS bill_exec(
    #                     id BIGINT NOT NULL AUTO_INCREMENT,
    #                     name VARCHAR(255),
    #                     title VARCHAR(255),
    #                     year INT(11),
    #                     salary DECIMAL(11,2),
    #                     bonus DECIMAL(11,2),
    #                     stock_awards DECIMAL(11,2),
    #                     option_awards DECIMAL(11,2),
    #                     RSUs DECIMAL(11,2),
    #                     nonequity_incentive_plan_compensation DECIMAL(11,2),
    #                     change_in_pension_value_and_nonqualified_deferred_compensation DECIMAL(11,2),
    #                     securities_underlying_options DECIMAL(11,2),
    #                     all_other DECIMAL(11,2),
    #                     total DECIMAL(11,2),
    #                     remainder DECIMAL(11,2),
    #                     accession VARCHAR(255),
    #                     cik INT(11),
    #                     file_year INT(11),
    #                     KEY(id)
    #           )'''
    # cursor.execute(sql)
    # db.close()
    #
    # print "exec_test2 DB created"

    #txtpath = '/local/bill_test/'
    txtpath = ''
    with open(txtpath + 'remainder.txt', 'w') as f:
        f.write("+++++++ \n")
    with open(txtpath + 'error_file.txt', 'w') as tf:
        tf.write("++++++ \n")
    with open('test.csv', 'w') as cf:
        writer = csv.writer(cf)
        writer.writerow(['test'])

    #path = '/local/def14a_extract/comp_tables_two/*.txt'
    # outpath = '/local/bill_test/files/'
    path = '/Users/bill/PycharmProjects/BeauSoupTest/comp_table/*.txt'
    # for filename in glob.glob(path):
    #     csvname = os.path.basename(filename)
    #     csvname = os.path.splitext(csvname)[0]
    #     # filename = ''.join(('file:///', filename))
    #     accession = csvname.split('_')[0]
    #     #csvname = ''.join((outpath, csvname, '.csv'))
    #     #print csvname
    #     with open(filename, 'r') as textfile:
    #         cik = int(textfile.readline())
    #         file_year = int(textfile.readline())
    #     try:
    #         data = get_table(filename)
    #         table = rearrange_data(data, csvname)
    #         for row in table:
    #             if row[2]:
    #                 pass
    #             else:
    #                 raise Exception
    #         # writeToCSV([[csvname]], 'test.csv', 'a')
    #         # writeToCSV(table, 'test.csv', 'a')
    #

            # query = "INSERT INTO bill_exec(`name`, `year`, `title`, `salary`,`bonus`,`stock_awards`,`option_awards`, `RSUs`, " \
            #     "`nonequity_incentive_plan_compensation`,`change_in_pension_value_and_nonqualified_deferred_compensation`,  " \
            #     "`all_other`,  `securities_underlying_options`," \
            #     "`remainder`, `total`," \
            #     " `cik`, `accession`, `file_year` )"\
            #     "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # #
    #         # db = MySQLdb.connect("localhost", "root", "Edgar20!4", "def14a")
    #         # cursor = db.cursor()
    #         # for row in table[1:]:
    #         #     row.extend([cik, accession, file_year])
    #         #     try:
    #         #         cursor.execute(query, tuple(row))
    #         #         db.commit()
    #         #         print "db_updated"
    #         #     except MySQLdb.Error as e:
    #         #         db.rollback()
    #         #         print e
    #         # cursor.close()
    #         # print 'Done'
    #     except:
    #         with open('/local/bill_test/error_file.txt', 'a') as tf:
    #             tf.write(csvname + "\n")





    #Test for 1 file
    filename = '/Users/bill/PycharmProjects/BeauSoupTest/comp_tables_two/0000892569-08-000989_948708_1.txt'
    csvname = os.path.basename(filename)
    csvname = os.path.splitext(csvname)[0]
    data = get_table(filename)
    writeToCSV([[filename]], 'test.csv', 'a')
    writeToCSV(data, 'test.csv', 'a')
    table = rearrange_data(data, csvname)
    writeToCSV(table, 'test.csv', 'a')


