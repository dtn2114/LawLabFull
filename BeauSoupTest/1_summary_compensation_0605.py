#!/usr/bin/python

from bs4 import *
import copy
import itertools
import json
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
import datetime
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

#FUNCTIONS
def adjust_col_strings(raw, rowspan):
    col_strings = []
    # print raw
    for st in raw:
        # st = st.encode('utf8').strip()
        processed = st.replace(u'\u2014', '-').replace(u'\x97', '-').replace(u'\uFE58', '-').encode('ascii',
                                                                                                    'replace').replace('?', ' ').replace('\n', ' ')
        # processed = processed.encode('utf8')
        if processed.strip():
            # print col_strings
            col_strings.append(processed)
    # print st
    if len(col_strings) > rowspan:
        col_strings[rowspan - 1] = ' '.join(col_strings[rowspan - 1:])
    else:
        for i in range(len(col_strings), rowspan):
            col_strings.append('')
    return col_strings

def add_two_numberstr(a, b):
    if len(a.split()) > 1 and len(b.split()) >1:
        a = [e.strip('-') for e in a.split()]
        b = [e.strip('-') for e in b.split()]
        combined = [list(e) for e in itertools.izip_longest(a,b, fillvalue = '')]
        # print combined
        combined = [[''.join([k.strip() for k in i.split(',')]) for i in e] for e in combined]
        # print combined
        combined = [str(int(sum([float(i) for i in filter(bool,e)]))) if filter(bool,e) else '-' for e in combined]
        # print combined
        return str(' '.join(combined))
    else:
        # print a,b
        a = a.strip('-')
        b = b.strip('-')
        a = ''.join([e.strip() for e in a.split(',')])
        b = ''.join([i.strip() for i in b.split(',')])
        return str(float(a) + float(b))

def balance_rows(data, num_col):
    for i, row in enumerate(data):
        diff = num_col - len(row)
        if diff:
            row = row + [''] * diff
        data[i] = row
    return data

def convert_negative_number(st):
    return re.sub('^\((-?\d+)(\,?\d+)\)?$', r'-\1\2', st)

def convert_underscore(data):
    return [[re.sub('^(\_+)$', '-', cell) for cell in row] for row in data]

def convert_nil(data):
    for i, row in enumerate(data):
        data[i][1:] = ['0' if 'nil' in cell.lower() else cell for cell in row[1:]]
    return data

def clean_data_first_pass(data):
    data = remove_apple_footnote(data)
    data = remove_whitespace(data)
    data = remove_stars(data)
    data = remove_dollar(data)
    data = convert_underscore(data)
    return data

def clean_data(data):
    # print_row(data)
    data = remove_footnote(data)
    # print_row(data)
    data = remove_dollar(data)
    # print_row(data)
    data = remove_empty_pipe(data)
    # print data
    data = remove_empty_data_cols(data)
    data = convert_nil(data)
    return data

def classify_rows(data, pointer=0):
    # print 'pointer', pointer
    # print_row(data[pointer:])
    for i, row in enumerate(data[pointer:]):
        if is_data_row(row):
            # print_row(data[:4])
            # print row,i
            # print data[i-2]
            j = i
            i = i+pointer
            #print is_empty(data[i-1][1])
            if 'name' in data[i-1][0].lower():
                return i - 1
            elif 'position' in data[i-1][0].lower():
                return i - 1
            elif any(['salary' in e.lower() for e in data[i-1]]):
                return i - 1
            elif 'name' in data[i-2][0].lower() or 'position' in data[i-2][0].lower():
                return i - 2
            elif 'name' in data[i-3][0].lower() or 'position' in data[i-3][0].lower():
                return i - 1
            elif 'name' in data[i-4][0].lower() or 'position' in data[i-4][0].lower():
                return i - 1
            elif 'name' in data[i-5][0].lower() or 'position' in data[i-5][0].lower():
                return i - 1
            # elif not is_empty(data[i-1][1]):
            #     return pointer+i - 1
            else:
                #print i-10
                return classify_rows(data, pointer+j+1)

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

def create_titles2(data):
    header_ind = classify_rows(data)
    #print(header_ind)
    #print data[header_ind+1:]
    #print data[header_ind+19][0]
    #print data
    if header_ind > -1 or is_empty(data[header_ind+19][0]):
        #print data
        return data
    else:
        header_ind = header_ind + 18
        #print data[header_ind]
        recognizer = data[header_ind+1][1]
        count = header_ind+1
        #orig_year = get_orig_year(data)
        result = []
        result.append(data[0])
        #print data
        #print data[header_ind+2:]
        for i, row in enumerate(data[header_ind+2:]):
            if i <= len(data[header_ind+4:]):
                if row[1] and data[i+1+header_ind+2][1] is recognizer:
                    #print data[i+header_ind+3]
                    one_person = data[count:i+header_ind+3]
                    zipped = zip(*one_person)
                    zipped = [list(a) for a in zipped]
                    zipped[0][0] = zipped[0][0]+'|'
                    combined = [[' '.join(a) for a in zipped]]
                    #print combined
                    #combined = [list(a) for a in combined]
                    result.append(combined[0])
                    count = i+header_ind+3
            else:
                if i == len(data[header_ind+3:]):
                    last_person = data[count:i+header_ind+3]
                    zipped = zip(*last_person)
                    zipped = [list(a) for a in zipped]
                    zipped[0][0] = zipped[0][0]+'|'
                    combined = [[' '.join(a) for a in zipped]]
                    #combined = [list(a) for a in combined]
                    result.append(combined[0])
                    count = i+header_ind+3
        #print result
        return result

def create_titles(data):
    orig_year = get_orig_year(data)
    #print orig_year
    if '-' in orig_year:
        orig_year = orig_year.split('-')[0]
    else:
        orig_year = orig_year
    #titles = []
    title = []
    count = 1
    name = ''
    # print_row(data)
    for i, row in enumerate(data):
        if 'year' in row[1].lower() or 'yr' in row[1].lower() or 'fy' in row[1].lower():
            if i == 0:
                data[i].append('Title')
            else:
                raise Exception('Headers are not on row 0')
        else:
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
    # print_row(data)
    return data

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

def find_total(line):
    if filter(None, line[3:]):
        total = sum(float(i) for i in filter(None, line[3:]))
        return Decimal(total)
    else:
        return None

def get_name(data):
    for i, row in enumerate(data):
        if i == 0:
            pass
        else:
            if 'year' in row[1].lower() or 'yr' in row[1].lower():
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
    return remove_pipe(data)

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
        # print row
        if is_data_row(row):
            return row[1]
    else:
        raise Exception ('orig_year')

def getFullness(row):
    fullness = 0
    for val in row:
        if val:
            fullness += 1
    return fullness

def get_names_titles(data):
    table = [data[i][0] for i, row in enumerate(data)]
    return table

def is_data_row(row):
    #joined = ''.join(row[1:])
    row = [cell.strip() for cell in row]
    row = filter(bool, row)
    for cell in row[1:]:
        if 'year' in cell.lower():
            #print row
            return False
        if percent_digit_or_dash(cell.split()[0]) > 0.9:
            # print cell
            return True
    return False

def is_empty(st):
    if not st:
        return True
    else:
        return False

def is_number(s):
    try:
        s = s.strip('$')
        s = s.strip('-')
        s = ''.join([a.strip() for a in s.split(',')])
        float(s)
        return True
    except ValueError:
        return False

def percent_digit_or_dash(st):
    stLen = len(st)
    st = re.sub(u'\-', ' ', st)
    if stLen == 0:
        return 0.0
    numDigits = sum([1 for x in st if x.isdigit() or x == '-' or x == '$' or x == '.' or x ==
                     ','])

    percent = float(numDigits)/float(stLen)
    return percent

def print_row(data):
    for row in data:
        print len(row),row

def rebalance_rows(data):
    data_2 = copy.deepcopy(data)
    num_col = len(filter(bool, data_2[0][1:]))
    for i, row in enumerate(data_2):
        temp_row = filter(bool, row[1:])
        if len(temp_row) is num_col:
                data_2[i][1:] = filter(bool, row[1:])
        else:
            if len(temp_row) is not 0:
                return data
            else:
                pass
    return data_2

def remove_apple_footnote(data):
    # print data
    data = [[re.sub(u'\(\s?\d*\s', ' ', cell+' ') for cell in row] for row in data]
    #print data
    return [[re.sub(u'\s\)', ' ', cell) for cell in row] for row in data]

def remove_whitespace(data):
    data = [[re.sub(u'^\s*', '', cell) for cell in row] for row in data]  # remove from the start
    data = [[re.sub(u'\s*$', '', cell) for cell in row] for row in data]  # remove from the end
    return [[re.sub(u'\s+', ' ', cell) for cell in row] for row in data]  # remove from the middle

def remove_footnote(data):
    #remove things like (1), (2) footnotes
    # print data[1:,1:]
    # print_row(data)
    data = [[re.sub(u'(\d+)\s?[a-zA-Z]', r'\1', cell) if 'n/a' not in cell.lower() else cell for cell in row ] for row in data]
    # print_row(data)
    data = [[re.sub(u'(\d+)\(\d*\)\)?', r'\1', cell) for cell in row] for row in data]
    data = [[re.sub(u'\s\(\d+\)\)?\s', ' ', cell) for cell in row] for row in data]
    # print_row(data)
    return [[re.sub(u'\(\d*\)\)?', '-', cell) for cell in row] for row in data]

def remove_dollar(data):
    #remove dollar sign, hash sign.
    return [[re.sub(u'\(\$*\)|\(\#*\)|\$*', '', cell) for cell in row] for row in data]

def remove_empty_row(data):
    # print_row(data)
    #remove row with just name and no data
    lst = []
    default_len = len(data[0])
    # print default_len
    for i, row in enumerate(data):
        # print len(row),row
        if len(row) == default_len:
            if not is_data_row(row) and not any('year' in cell.lower() for cell in row) and not any('yr' in cell.lower() for cell in row):
                # print row
                lst.append(i)
            elif not row[1]:
                lst.append(i)
            else:
                # print row
                pass
        else:
            lst.append(i)
    # print lst
    # print data[lst[0]]
    lst = set(lst)
    return [v for i, v in enumerate(data) if i not in lst]

def remove_empty_pipe(data):
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if '|' in cell:
                cell = [elem.strip() for elem in cell.split('|')]
                cell = filter(bool, cell)
                data[i][j] = '|'.join(cell)
            else:
                pass
            if ')' in cell:
                cell = [elem.strip() for elem in cell.split(')')]
                cell = filter(bool, cell)
                data[i][j] = ')'.join(cell)
            else:
                pass
    return data

def remove_empty_cols_rows(data, keepSparse = True, duplicates = []):
    rows = None
    cols = None
    if duplicates:
        modify_duplicates = True
    else:
        modify_duplicates = False
    if modify_duplicates:
        rows = [i for i, row in enumerate(data) if not (any(row))]
        #print rows
    data = [list(row) for row in data if any(row)]
    # print data
    data = zip(*data)
    # print data
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
    # print data
    #data = [[cell for cell in row if any(cell)] for row in data]
    data = zip(*data)
    # print data
    data = [[cell.strip() for cell in row] for row in data]
    data = [list(row) for row in data if any(row)]
    data = zip(*data)
    data = [list(row) for row in data]
    # print data
    return data

def remove_non_exec_comp(data):
    # print_row(data[0])
    # print data
    # for row in data[0]:
    for row in data:
        if any(['%' in cell.lower() for cell in row]):
            # print row
            raise Exception('Percent in header row')
        elif any(['%' in cell.lower() for cell in row]):
            raise Exception('Year not in header row')
    for cell in data[0]:
        # if not any('year' in cell.lower)
        if 'year' in cell.lower():
            # print cell
            return data
        elif 'salary' in cell.lower():
            return data
        elif 'fy' in cell.lower():
            return data
        elif 'yr' in cell.lower():
            return data
    # raise Exception

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
        #print header_ind, last_row
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
                    # print header_ind
                    # print data[header_ind]
                    for col in cols:
                        # print col
                        # entries = row[col].split()
                        # colStr.append(entries)
                        if row[col].strip():
                            # print row[col], "2"
                            # print type(colStr), "1"
                            if is_empty(colStr.strip()):
                                # print colStr, 'here'
                                colStr += row[col]
                            elif is_number(row[col].split()[0]) and is_number(colStr.split()[0]):
                                colStr = add_two_numberstr(colStr, row[col])
                            elif not is_number(row[col].split()[0]) and not is_number(colStr.split()[0]):
                                colStr += row[col]
                            elif not is_number(row[col].split()[0]) and is_number(colStr.split()[0]):
                                colStr = colStr
                            elif is_number(row[col].split()[0]) and not is_number(colStr.split()[0]):
                                colStr = row[col]
                            else:
                                colStr += row[col]
                        else:
                            colStr += row[col]
                        # print colStr
                    rowList = list(row)
                    rowList[first_col] = colStr
                    rowTuple = tuple(rowList)
                    data[i] = rowTuple
    #print data
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

def remove_pipe(data):
    return [[re.sub(u'\|?\)?', '', cell) for cell in row] for row in data]

def remove_slash(st):
    if '/' in st.lower():
        st = st.split('/')
        st = str(sum(float(i) for i in filter(bool, st) if filter(bool,st)))
        return st
    else:
        return st

def remove_stars(data):
    return [[re.sub(u'\**', '', cell) for cell in row] for row in data]

def replace_tag(elem):
    soup=elem
    if soup.br is not None:
        soup = str(soup)
        soup = re.sub(r"</?br?/?>", "|", soup)
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
    header_ind = classify_rows(data)
    # print header_ind
    # print_row(data)
    # print header_ind, data[header_ind]
    #Split one line into two if year column has more than 1 year
    orig_year = data[header_ind+1][1]
    # print orig_year
    if '-' in orig_year:
        orig_year = orig_year.split('-')
    else:
        orig_year = orig_year.split()
    if len(orig_year) > 1:
        # print_row(data)
        lines = []
        # print orig_year
        # lines.append()
        for i, row in enumerate(data):
            if is_data_row(row):
                # print row
                for j in range(1, len(row)):
                    row[j] = row[j].split()
                line = row[1:]
                # print line

                #line = zip(*line)
                line = list(itertools.izip_longest(*line, fillvalue = ''))
                # print(line)
                for k, entry in enumerate(line):
                    # print entry
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
        # print_row(lines)
        return lines
    else:
        return data

def strip_first_cell(data):
    if 'name' in data[0][0].lower():
        data[0][0] = 'name'
        return data
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
            # print super_header_text
            for point in duplicate:
                if point[0] == first_row:
                    # print data[point[0]][point[1]]
                    data[point[0]][point[1]] = super_header_text
    return data

def add_space(data):
    for i, row in enumerate(data):
        if is_number(row[0]):
            row.insert(0,'')
        else:
            pass
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
    # print soup
    # balance table using colspan, rowspan
    result = defaultdict(lambda: defaultdict(unicode))
    duplicates = []

    for row_i, row in enumerate(table.find_all('tr')):
        for col_i, col in enumerate(row.find_all(['td', 'th'])):
            # print col
            if col_i == 0:
                col = replace_tag(col)
            # print col
            colspan = int(col.get('colspan', 1))
            rowspan = int(col.get('rowspan', 1))
            while row_i in result and col_i in result[row_i]:
                col_i += 1
            is_duplicate = False
            if rowspan > 1 or colspan > 1:
                duplicate = []
                is_duplicate = True
            # print col

            col_strings = adjust_col_strings(col.strings, rowspan)
            # print col_strings
            # print col_strings
            for i in range(row_i, row_i + rowspan):
                for j in range(col_i, col_i + colspan):
                    if j == col_i:
                        # print col_strings
                        result[i][j] = col_strings[i - row_i]
                        # print result[i][j]
                    else:
                        result[i][j] = ''
                    if is_duplicate:
                        duplicate.append([i, j])
            if is_duplicate:
                duplicates.append(duplicate)
    # print result
    # print_row(result)
    data = []
    num_col = 0
    for i, row in sorted(result.items()):
        cols = []
        # print row
        for j, col in sorted(row.items()):
            cols.append(col.strip())
        if len(cols) > num_col:
            num_col = len(cols)
        # print cols
        data.append(cols)
    # print_row(data)
    data = add_space(data)
    # print_row(data)
    data = balance_rows(data, num_col)
    # print_row(data)
    data = clean_data_first_pass(data)
    # print_row(data)
    data, duplicates = remove_empty_cols_rows(data, duplicates=duplicates)
    # print duplicates
    # print_row(data)
    name_title = get_names_titles(data)
    # print name_title
    header_ind = classify_rows(data)
    # print_row(data)
    # print 'header row', header_ind, data[header_ind]
    # if header_ind < -1:
    #     header_ind = header_ind + 18
        # print header_ind
    # print_row(data)
    # print data[header_ind+1]
    if header_ind is not None:
        data = write_super_headers(duplicates, data, header_ind)
        # print_row(data)
        data = remove_horizontal_header_duplicates(duplicates, data, header_ind)
        # print_row(data)
        data = combine_headers(data, header_ind)
    # print_row(data)
    data = clean_data(data)
    # print_row(data)
    data = rebalance_rows(data)
    # print_row(data)
    # data = create_titles2(data)
    # print_row(data)
    # print data
    data = split_line(data)
    # print_row(data)
    data = create_titles(data)
    # print_row(data)
    data = get_name(data)
    # print_row(data)
    data = remove_empty_row(data)
    # print_row(data)
    data = remove_non_exec_comp(data)
    data = [[re.sub('^(-?\d+)(\,?\d+)\s([0-9])$', r'\1\2', cell) for cell in row] for row in data]
    return data, name_title

def match_header_dict(data_headers, filename, remainderfile):
    headers_dict = {'name': [], 'year': [], 'title': [], 'salary': [], 'bonus': [], 'stock': [], 'option': [],
                    'restricted': [], 'incentive': [], 'pension': [], 'other': [], 'securities': [], 'remainders': []}
    total_headers = len(data_headers)
    headers_found = []
    # print data_headers

    for j, header_j in enumerate(data_headers):
        if 'total' in header_j.lower():
            headers_found.append(j)
            continue
        for index, (header_i, i) in enumerate(headers_dict.items()):
            if header_i in header_j.lower():
                # if 'option' in header_j.lower():
                #     print j
                if 'option' == header_i and 'securities' in header_j.lower():
                    pass
                elif 'stock' == header_i and 'option' in header_j.lower():
                    pass
                elif 'stock' == header_i and 'restricted' in header_j.lower():
                    pass
                elif 'year' == header_i and j not in [1,2]:
                    pass
                elif 'incentive' == header_i and 'non' not in header_j.lower():
                    pass
                elif 'pension' == header_i and 'without' in header_j.lower():
                    pass
                elif 'stock' == header_i and 'non' in header_j.lower():
                    headers_dict[header_i].append(j)
                    headers_found.append(j)
                else:
                    # print header_i
                    headers_dict[header_i].append(j)
                    headers_found.append(j)
        if 'deferred' in header_j.lower() and 'pension' not in header_j.lower():
            headers_dict['pension'].append(j)
            headers_found.append(j)
        if 'rsu' in header_j.lower() and 'restricted' not in header_j.lower():
            headers_dict['restricted'].append(j)
            headers_found.append(j)
        if 'share' in header_j.lower() and 'stock' not in header_j.lower() and 'option' not in header_j.lower():
            headers_dict['stock'].append(j)
            headers_found.append(j)
        if 'yr' in header_j.lower() and j == 1:
            headers_dict['year'].append(j)
            headers_found.append(j)
    # print data_headers
    # print headers_dict
    with open(remainderfile, 'a') as textFile:
        textFile.write(filename + "\n")
        for i in range(0, total_headers):
            if i not in headers_found:
                # print data_headers[i]
                headers_dict['remainders'].append(i)
                textFile.write("\t" + data_headers[i]+"\n")
    return headers_dict

def rearrange_data(data, filename, remaindertextfile):
    # print_row(data)
    data = strip_first_cell(data)
    table = []
    fixed_header = ['name', 'year', 'title', 'salary', 'bonus', 'stock', 'option',
                    'restricted', 'incentive', 'pension', 'other', 'securities', 'remainders', 'total']
    table.append(fixed_header)
    # print data
    headers_dict = match_header_dict(data[0], filename, remaindertextfile)
    # print headers_dict
    for j, row in enumerate(data[1:]):
        #print row
        line = []
        for e, header_e in enumerate(table[0][:3]):
            cell_lst = headers_dict[header_e]
            # print headers_dict['year']
            if not cell_lst:
                if header_e == 'year':
                    raise Exception('Year Column are empty')
                else:
                    value = ''
            else:
                if len(cell_lst) > 1:
                    raise Exception('More than 1' + header_e)
                else:
                    if header_e == 'year':
                        # print row[cell_lst[0]]
                        if len(row[cell_lst[0]]) >4:
                            # print row[cell_lst[0]]
                            raise Exception('Year are next to each other')
                        else:
                            if len(row[cell_lst[0]]) == 2:
                                if Decimal(row[cell_lst[0]]) < 50:
                                    value = '20'+row[cell_lst[0]]
                                else:
                                    value = '19'+row[cell_lst[0]]
                            else:
                                value = row[cell_lst[0]]
                    else:
                        value = row[cell_lst[0]]
            line.append(value.strip())
        # total = None
        for i, header_i in enumerate(table[0][3:(len(table[0])-1)]):
            # print headers_dict
            cell_lst = headers_dict[header_i]
            # print cell_lst
            # print header_i
            value = None
            if not cell_lst:
                pass
            else:
                if len(cell_lst) > 1:
                    # print header_i
                    for k in cell_lst:
                        amount = row[k].strip('-')
                        amount = ''.join([a.strip() for a in amount.split(',')])
                        amount = convert_negative_number(amount)
                        if amount:
                            if 'n/a' in amount.lower() or 'not applicable' in amount.lower():
                                if value is None:
                                    pass
                                else:
                                    value = value
                            else:
                                if value is None:
                                    amount = remove_slash(amount)
                                    value = Decimal(amount)
                                else:
                                    amount = remove_slash(amount)
                                    value += Decimal(amount)
                        else:
                            if value is None:
                                value = None
                            else:
                                value = value
                else:
                    amount = row[cell_lst[0]].strip('-')
                    amount = ''.join([a.strip() for a in amount.split(',')])
                    # amount = ''.join([a.strip() for a in amount.split('.')])
                    amount = convert_negative_number(amount)

                    # print amount
                    if amount:
                        if 'n/a' in amount.lower() or 'not applicable' in amount.lower():
                            if value is None:
                                pass
                            else:
                                value = value
                        else:
                            amount = remove_slash(amount)
                            value = Decimal(amount)
                    else:
                        pass
            line.append(value)
        # print total
        total = find_total(line)
        # print total2
        line.append(total)
        #print line
        table.append(line)
    return table

#0001108017-06-000129_1126216_2


if __name__ == '__main__':
    txtpath = ''
    with open(txtpath + 'remainder_0608.txt', 'w') as f:
        f.write("+++++++ \n")
    with open(txtpath + 'error_file_0608.txt', 'w') as tf:
        tf.write("++++++ \n")
    # with open('test.csv', 'w') as cf:
    #     writer = csv.writer(cf)
    #     writer.writerow(['test'])

    # #Test for 1 file
    filename = '/local/bill_test/exec_comp_tables_final/'
    # filename = '/Users/bill/PycharmProjects/BeauSoupTest/textfiles/PFE/'
    accession_cik = '0001193125-11-073431_78003_4'
    filename = filename + accession_cik + '.txt'
    csvname = os.path.basename(filename)
    csvname = os.path.splitext(csvname)[0]
    data, name_title = get_table(filename)
    # print_row(data)
    # data = [['Name and Principal Position|(a)', 'Year (b', 'Salary (c', 'Bonus (d', 'Stock Awards --- (e', 'Option Awards -- (f', 'Non-Equity Incentive Plan Compensation (g', 'Change in Pension Value and Non-Qualified Deferred Compensation Earnings (h', 'All Other Compensation (i', 'Total  (j'],['Indra K. Nooyi|Director; Chairman of the Board and|Chief Executive Officer', '2007 2006', '1,300,000 964,413', '0 0', '3,231,973 2,006,876', '2,829,423 2,353,440', '3,200,000 3,000,000', '825,085 898,884', '92,215 153,506', '11,478,696 9,377,119']]
    # data = split_line(data)
    # # print_row(data)
    # data = create_titles(data)
    # # print_row(data)
    # data = get_name(data)
    # data = remove_empty_row(data)
    # print_row(data)
    #  writeToCSV([[filename]], 'test.csv', 'a')
    # writeToCSV(data, 'test.csv', 'a')
    table = rearrange_data(data, csvname, 'remainder_0608.txt')
    # print_row(table)
    # writeToCSV(table, 'test.csv', 'a')

    db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "def14a")
    cursor = db.cursor()
    query = "INSERT INTO bill_exec_0608(`name`, `year`, `title`, `salary`,`bonus`,`stock_awards`," \
                        "`option_awards`, `RSUs`, " \
                    "`nonequity_incentive_plan_compensation`,`change_in_pension_value_and_nonqualified_deferred_compensation`,  " \
                    "`all_other`,  `securities_underlying_options`," \
                    "`remainder`, `total`," \
                    " `cik`, `accession`, `file_date` )"\
                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    accession = accession_cik.split('_')[0]
    cik = accession_cik.split('_')[1]
    file_date = '2011-03-22'
    #Insert data into table 1.
    for row in table[1:]:
        # if '2013' in row[1]:
        #     pass
        # else:
        row.extend([cik, accession, file_date])
        try:
            cursor.execute(query, tuple(row))
            db.commit()
            print "db_updated"
        except MySQLdb.Error as e:
            db.rollback()
            print e
    print 'Done'

    # #TEST MULTIPLE FILE LOCALLY
    # path = '/Users/bill/PycharmProjects/BeauSoupTest/textfiles/test_files/*.txt'
    # for filename in glob.glob(path):
    #     csvname = os.path.basename(filename)
    #     csvname = os.path.splitext(csvname)[0]
    #     accession = csvname.split('_')[0]
    #     with open(filename, 'r') as textfile:
    #         cik = int(textfile.readline())
    #         file_date = textfile.readline()
    #         file_date = datetime.datetime.strptime(file_date.strip(), '%Y%m%d').date()
    #     print csvname
    #     writeToCSV([[csvname]], 'test.csv', 'a')
    #     try:
    #         data, name_title = get_table(filename)
    #         writeToCSV(data, 'test.csv', 'a')
    #         # print data
    #         try:
    #             table = rearrange_data(data, csvname, txtpath+'remainder_0607.txt')
    #             writeToCSV(table, 'test.csv', 'a')
    #             print_row(table)
    #
    #         except Exception, e:
    #             #print (csvname + ' ' + str(e) + ' rearrange')
    #             #print data
    #             with open(txtpath + 'error_file_0607.txt', 'a') as tf:
    #                 tf.write(csvname + ' '+ str(e) + "\n")
    #     except Exception, e:
    #         #print (csvname +' '+ str(e) + ' get_table')
    #         with open(txtpath + 'error_file_0607.txt', 'a') as tf:
    #             tf.write(csvname + ' '+ str(e)+ "\n")


    # db = MySQLdb.connect("localhost", "root", 'Edgar20!4', "def14a")
    # cursor = db.cursor()
    #
    # sql = '''CREATE TABLE IF NOT EXISTS bill_exec_0607(
    #                     id BIGINT NOT NULL AUTO_INCREMENT,
    #                     name TEXT,
    #                     title TEXT,
    #                     year INT(11),
    #                     salary DECIMAL(19,2),
    #                     bonus DECIMAL(19,2),
    #                     stock_awards DECIMAL(19,2),
    #                     option_awards DECIMAL(19,2),
    #                     RSUs DECIMAL(19,2),
    #                     nonequity_incentive_plan_compensation DECIMAL(19,2),
    #                     change_in_pension_value_and_nonqualified_deferred_compensation DECIMAL(19,2),
    #                     securities_underlying_options DECIMAL(19,2),
    #                     all_other DECIMAL(19,2),
    #                     total DECIMAL(19,2),
    #                     remainder DECIMAL(19,2),
    #                     accession VARCHAR(255),
    #                     cik INT(11),
    #                     file_date DATE,
    #                     KEY(id)
    #           )'''
    # table2 = '''CREATE TABLE IF NOT EXISTS bill_name_0607(
    #                     id BIGINT NOT NULL AUTO_INCREMENT,
    #                     name_title TEXT,
    #                     accession VARCHAR(255),
    #                     cik INT(11),
    #                     file_date DATE,
    #                     KEY(id)
    #           )'''
    # cursor.execute(sql)
    # cursor.execute(table2)
    # #db.close()
    #
    # print "bill_exec DB created"




    # # txtpath = '/local/bill_test/'
    # txtpath = ''
    # with open(txtpath + 'remainder_0607.txt', 'w') as f:
    #     f.write("+++++++ \n")
    # with open(txtpath + 'error_file_0607.txt', 'w') as tf:
    #     tf.write("++++++ \n")
    #
    #
    # # path = '/local/def14a_extract/tables_pass_three/*.txt'
    # path = '/local/bill_test/exec_comp_tables_final/*.txt'
    # # path = '/Users/bill/PycharmProjects/BeauSoupTest/textfiles/bill_friday_tables/*.txt'
    # #path = '/Users/bill/PycharmProjects/BeauSoupTest/comp_table/*.txt'
    # for filename in glob.glob(path):
    #     csvname = os.path.basename(filename)
    #     csvname = os.path.splitext(csvname)[0]
    #     accession = csvname.split('_')[0]
    #     with open(filename, 'r') as textfile:
    #         cik = int(textfile.readline())
    #         file_date = textfile.readline()
    #         file_date = datetime.datetime.strptime(file_date.strip(), '%Y%m%d').date()
    #     # print csvname
    #     # writeToCSV([[csvname]], 'test.csv', 'a')
    #     try:
    #         data, name_title = get_table(filename)
    #         # writeToCSV(data, 'test.csv', 'a')
    #         try:
    #             table = rearrange_data(data, csvname, txtpath+'remainder_0607.txt')
    #             # writeToCSV(table, 'test.csv', 'a')
    #
                # query = "INSERT INTO bill_exec_0607(`name`, `year`, `title`, `salary`,`bonus`,`stock_awards`," \
                #         "`option_awards`, `RSUs`, " \
                #     "`nonequity_incentive_plan_compensation`,`change_in_pension_value_and_nonqualified_deferred_compensation`,  " \
                #     "`all_other`,  `securities_underlying_options`," \
                #     "`remainder`, `total`," \
                #     " `cik`, `accession`, `file_date` )"\
                #     "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #
    #             query2 = "INSERT INTO bill_name_0607(`name_title`, `cik`, `accession`, `file_date` )"\
    #                 "VALUES(%s, %s, %s, %s)"
    #
    #
    #             # db = MySQLdb.connect("localhost", "root", "Edgar20!4", "def14a")
    #             # cursor = db.cursor()
    #
    #             #Insert data into table 2
    #             try:
    #                 line = []
    #                 name_title = json.dumps(name_title)
    #                 line.append(name_title)
    #                 line.extend([cik, accession, file_date])
    #                 cursor.execute(query2, tuple(line))
    #                 db.commit()
    #             except MySQLdb.Error as e:
    #                 db.rollback()
    #                 print e
    #
                # #Insert data into table 1.
                # for row in table[1:]:
                #     row.extend([cik, accession, file_date])
                #     try:
                #         cursor.execute(query, tuple(row))
                #         db.commit()
                #         print "db_updated"
                #     except MySQLdb.Error as e:
                #         db.rollback()
                #         print e
                # print 'Done'
    #
    #         except Exception, e:
    #             #print (csvname + ' ' + str(e) + ' rearrange')
    #             #print data
    #             with open(txtpath + 'error_file_0607.txt', 'a') as tf:
    #                 tf.write(csvname + ' '+ str(e) + "\n")
    #     except Exception, e:
    #         #print (csvname +' '+ str(e) + ' get_table')
    #         with open(txtpath + 'error_file_0607.txt', 'a') as tf:
    #             tf.write(csvname + ' '+ str(e)+ "\n")
    #
    # db.close()
    # print 'Finally Done'

#Problem when the index is accidentally -1
#0000950152-08-006742_110621_1
#Data next to first title
#0001047469-13-004190_899051_1