#!/usr/bin/python
__author__ = 'bill'

import urllib2
from lxml import etree
import scraperwiki
import pdfquery
import textract


if __name__ == '__main__':
    # file_add = '/Users/bill/Downloads/Fall2015_Jobs/Dung_Nguyen_resume.pdf'
    file_add = '/Users/bill/PycharmProjects/BeauSoupTest/37325972.pdf'
    text = textract.process(file_add, method='tesseract')
    # pdf = pdfquery.PDFQuery(file_add)
    # pdf.load()
    # print type(pdf)
    # u=urllib2.urlopen("http://images.derstandard.at/2013/08/12/VN2p_2012.pdf")
    # print u
    # x=scraperwiki.pdftoxml(u.read())

    # print ord(x)
    # print x
    # r=etree.Element(x)
    # print r.tag
    # r.xpath('//page[@number="1"]')
    # r.xpath('//text[@left="64"]/b')[0:10]
