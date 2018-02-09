__author__ = 'bill'

from bs4 import *
import urllib2
import requests
import re
import csv
from decimal import *

if __name__ == '__main__':
    url = raw_input("Enter a URL of a document that has a general table of content: ")
    # csvfile = raw_input("Enter a name for the csv file including the .csv(ie. name.csv): ")
    #tesla link
    #url = "http://www.sec.gov/Archives/edgar/data/1318605/000119312511092509/ddef14a.htm"

    #google link
    #url = "http://www.sec.gov/Archives/edgar/data/1288776/000130817914000114/lgoogle2014_def14a.htm"

    #apple link
    #url = "http://www.sec.gov/Archives/edgar/data/320193/000119312515017607/d774604ddef14a.htm"

    #open the html doc
    data = urllib2.urlopen(url).read()
    # print data
    #turn into a soup object
    soup = BeautifulSoup(data)
    with open('html.txt', 'w') as f:
        f.write(str(soup))

    #Here I am using regular expression to find an object that has a href tag and text on "Summary Compensation Table"
    #regex is used to safeguard against non-connecting string of Summary Compensation Table
    # found_key = soup.find(text=re.compile('\s*Summary\s*Compensation\s*Table'), href = True)
    # #print(found_key)
    #
    # #find the unique href that is associated with the summary compensation table
    # table_key = str(found_key.get('href')).strip('#')
    # #print(type(table_key))
    #
    # #Use the href to go to the header of the table
    # found_key = soup.find("a", {'name' : table_key})
    #print(found_key)


    #found_key.find_next('tr').extract() #this line only apply to this document to improve look

    #FUNCTIONS
    #This function check if the a string is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#This function turns any string of dollar values to a decimal
def decimal_dollar(row):
    for i in range(len(row)):
        row[i]=row[i].replace(',','')
        #print(i,type(i),is_number(i))
        if is_number(row[i]):
            row[i]=Decimal(row[i])
            #print(i,type(i))
    #print(row[7],type(row[7]))
    return row

#OUTPUT into one single table
# table = found_key.find_next('table') #find the next table using the table_key
# with open(csvfile, 'wb') as f:
#     writer = csv.writer(f)
#     for trs in table.find_all('tr'):
#         tds = trs.find_all('td')
#         row = [elem.text.strip().encode('utf-8') for elem in tds] #encode from unicode to utf-8
#         row= decimal_dollar(row)
#         #print row
#         writer.writerow(row)http://brokercheck.finra.org/Firm/Summary/146999