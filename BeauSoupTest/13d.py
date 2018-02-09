#!/usr/bin/python
#__author__ = 'bill'

import os
import glob
import re
from bs4 import *
import unicodedata


def find_item():
    path = '/home/znagler/13d_scrape/sampleset/a*.txt'
    # path = '/Users/bill/PycharmProjects/BeauSoupTest/13d_scrape/*.txt'
    count = 0
    for filename in glob.glob(path):
        count+=1
        #csvname = os.path.basename(filename)
        #print csvname
        page_raw_text = open(filename).read()

        # xml_start = '<SEC-HEADER>'
        # xml_end = '</SEC-HEADER>'
        item1 = re.compile('Item\s*1\s*.\s*Security\s*and\s*Issuer', re.IGNORECASE)
        item2 = re.compile('Item\s*2\s*.\s*Identity\s*and\s*Background', re.IGNORECASE)
        item3 = re.compile('Item\s*3\s*.\s*Source\s*and\s*Amount\s*of\s*Funds\s*or\s*Other\s*Consideration', re.IGNORECASE)
        item4 = re.compile('Item\s*4\s*.\s*Purpose\s*of\s*Transaction', re.IGNORECASE)
        item5 = re.compile('Item\s*5\s*.\s*Interest\s*in\s*Securities\s*of\s*the\s*Issuer', re.IGNORECASE)
        item6 = re.compile('Item\s*6\s*.\s*Contracts\s*,\s*Arrangements\s*,\s*Understandings\s*or\s*Relationships\s*with\s*Respect\s*to\s*Securities\s*of\s*the\s*Issuer', re.IGNORECASE)
        item7 = re.compile('Item\s*7\s*.\s*Material\s*to\s*Be\s*Filed\s*as\s*Exhibits', re.IGNORECASE)
        end = re.compile('Signature(s)*', re.IGNORECASE)

        # xml_docs_start = [m.start() for m in re.finditer(xml_start, page_raw_text)]
        # xml_docs_end = [m.start() for m in re.finditer(xml_end, page_raw_text)]
        # #print xml_docs_start, xml_docs_end
        # doc_start = xml_docs_start[0] + len(xml_start)
        # doc_end = xml_docs_end[0]

        soup = BeautifulSoup(page_raw_text)
        page_raw_text = soup.get_text()
        page_raw_text = unicodedata.normalize('NFKD', page_raw_text).encode('ascii', 'ignore')
        item1 = re.search(item1, page_raw_text)
        item2 = re.search(item2, page_raw_text)
        item3 = re.search(item3, page_raw_text)
        item4 = re.search(item4, page_raw_text)
        item5 = re.search(item5, page_raw_text)
        item6 = re.search(item6, page_raw_text)
        item7 = re.search(item7, page_raw_text)
        end = re.search(end, page_raw_text)
        ls = [item1, item2, item3, item4, item5, item6, item7, end]
        ls = [i for i in ls if i]
        #print "number of items", len(ls) -1
        dict = {}
        for i in range(0,len(ls)-1):
            dict["Item{0}".format(i)] = find_between(page_raw_text, ls[i].group(0), ls[i+1].group(0))
            # print dict
            # Item1 = find_between(page_raw_text, item1.group(0), item2.group(0))
            # Item2 = find_between(page_raw_text, item2.group(0), item3.group(0))
            # Item3 = find_between(page_raw_text, item3.group(0), item4.group(0))
            # Item4 = find_between(page_raw_text, item4.group(0), item5.group(0))
            # Item5 = find_between(page_raw_text, item5.group(0), item6.group(0))
            # Item6 = find_between(page_raw_text, item6.group(0), item7.group(0))
            # Item7 = find_between(page_raw_text, item7.group(0), end.group(0))
        # if end:
        #     count+= 1
    if "Item1" not in dict.items():
        print str(count) + ": " + filename
    # print count
        # break
        #print dict
        #print "Item 1: " + Item1
        #print "Item 2: " + Item2
        #print "Item 3: " + Item3
        #print "Item 4: " + Item4
        #print "Item 5: " + Item5
        #print "Item 6: " + Item6
        #print "Item 7: " + Item7

        #print item1.group(0), type(item1.group(0))

        # print type(page_raw_text)
        # print item1.pattern, type(item1.pattern)
        #find_between(page_raw_text, item1.pattern, item2.pattern)

def find_between(s, first, last):
    try:
        start = s.index( first ) + len(first)
        end = s.index( last, start)
        return s[start:end]
    except Exception, e:
        print first, e
        return ""
def find_cusip():
    #   path = '/Users/bill/PycharmProjects/BeauSoupTest/textfiles/bill_friday_tables/*.txt'
    path = '/Users/bill/PycharmProjects/BeauSoupTest/13d_scrape/0001193125-04-140598.txt'
    i = 0
    j = 0
    for filename in glob.glob(path):

        csvname = os.path.basename(filename)
        #print csvname
        data = open(filename).read()
        search_html = re.search(r'((?i)<HTML>)', data)
        if search_html:
            i+=1
            # print filename
            #search_match = re.search(r'(\(*CUSIP\s+(?i)Number\)*)', data)
            soup = BeautifulSoup(data)
        # print soup
            found_key = soup.find('p',text = re.compile(r'(\(*CUSIP\s+(?i)Number\)*)'))
            if found_key:
                # print found_key
                print filename
                cusip = found_key.previous_sibling.previous_sibling.previous_sibling
                # for sibling in found_key.next_siblings:
                #     print(repr(sibling))
                print cusip

        # if not search_match:
        #     i += 1
        #     print filename

    print " i is " + str(i), " j is " + str(j)


if __name__ == '__main__':
    find_item()

