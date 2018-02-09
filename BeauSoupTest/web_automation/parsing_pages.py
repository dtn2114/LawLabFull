__author__ = 'yutingchen'

import csv
from global_setting_parsing import *
from bs4 import BeautifulSoup
import os
import re
import glob

def initialize_company_csv(filename):
    """ create a new csv file and write an appropriate column header
    """

    col_header = [["ORGANIZATION CRD#","FULL LEGAL NAME(1A)","PRIMARY BUSINESS NAME(1B)",\
                      "LEGAL NAME CHANGE?(1C)","SEC#(1D)","CRD#(1E)","MAIN OFFICE STREET ADDRESS 1(1F)","MAIN OFFICE STREET ADDRESS2(1F)",\
                    "MAIN OFFICE CITY(1F)","MAIN OFFICE STATE(1F)","MAIN OFFICE COUNTRY(1F)","MAIN OFFICE POSTAL CODE(1F)","PRIVATE RESIDENCE(1F)",\
                    "DAYS OF WEEK WORKED(1F(2))","NORMAL BUSINESS HOURS91F(2))","MAIN OFFICE TELEPHONE NUMBER(1F(3))","MAIN OFFICE FACSIMILE NUMBER(AF(4))",\
                    "MAIL ADDRESS NUMBER AND STREET1(1G)","MAIL ADDRESS NUMBER AND STREET2(1G)","MAIL ADDRESS CITY(1G)","MAIL ADDRESS STATE(1G)",\
                    "MAIL ADDRESS COUNTRY(1G)","MAIL ADDRESS POSTAL CODE(1G)","SOLE PROPRIETOR NUMBER AND STREET1(1H)","SOLE PROPRIETOR NUMBER AND STREET2(1H)",\
                    "SOLE PROPRIETOR CITY(1H)","SOLE PROPRIETOR STATE(1H","SOLE PROPRIETOR COUNTRY(1H)","SOLE PROPRIETOR POSTAL CODE(1H)","WEBSITE(1I)",\
                    "CCO NAME(1J)","CCO OTHER TITLES(1J)","CCO TELEPHONE#(1J)","CCO FACSIMILE#(1J)","CCO NUMBER AND STREET1(1J)","CCO NUMBER AND STREET2(1J)",\
                    "CCO CITY(1J)","CCO STATE(1J)","CCO COUNTRY(1J)","CCO ZIP CODE(1J)","CCO EMAIL(1J)","ARCP NAME(1K)","ARCP TITLES(1K)","ARCP TELEPHONE#(1K)",\
                    "ARCP FACSIMILE#(1K)","ARCP NUMBER AND STREET1(1K)","ARCP NUMBER AND STREET2(1K)","ARCP CITY(1K)","ARCP STATE(1K)","ARCP COUNTRY(1K)",\
                    "ARCP POSTAL CODE(1K)","ARCP EMAIL ADDRESS(1K)","1L","1M","1N","CIK#","1O","1P"]]

    try:
        outfile = open(filename, "wb")
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_ALL)
        for row in col_header:
            writer.writerow(row)
        outfile.close()
    except:
        raise

def write_company_info(data,filename):
    """ write data to a csv file
    """
    try:
        print filename
        outfile = open(filename, "a")
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_ALL)

        writer.writerow(data)
        outfile.close()
    except:
        raise


def extract_first_page(file):
    data = []
    soup = BeautifulSoup(file)
    table = soup.find('table',{'class':'PaperFormTableData'})
    if table == None: #meaning it's an ADV file
        return data

    primary_name = table.find('span',{'id':PRIMARY_NAME}).get_text()
    legal_name = table.find('span',{'id':FULL_LEGAL_NAME}).get_text()
    sec_number = table.find('span',{'id':SEC_NUM}).get_text()
    if sec_number == None:
        secNumber = table.find('span',{'id':SEC_NUM_EXEMPT}).get_text()
    crd_number = table.find('span',{'id':CRD_NUM}).get_text()
    data.append(crd_number)
    data.append(legal_name)
    data.append(primary_name)

    primary_change = 0
    legal_change = 0
    value_changed = 0
    checkboxes = table.find_all('img')
    for checkbox in checkboxes:
        if "your legal name" in checkbox.get_text():
            value = checkbox['alt']
            if not "not" in value:
                legal_change = 1
        elif "your primary business name" in checkbox.get_text():
            value = checkbox['alt']
            if not "not" in value:
                primary_change = 1
    if legal_change ==1 or primary_change ==1:
        value_changed = 1
    data.append(value_changed)
    data.append(sec_number)
    data.append(crd_number)

    sub_tables = table.find_all("table")
    address_table = sub_tables[0]

    address1 = ""
    address2 = ""
    city =""
    state=""
    country=""
    zip=""
    hours = ""
    telephone_num =""
    facsimile_num = ""

    spans = address_table.find_all("span")
    for span in spans:
        if "Number and Street 1" in span.parent.parent.get_text():
            address1 = span.get_text()
        elif "Number and Street 2" in span.parent.parent.get_text():
            address2 = span.get_text()
        elif "City" in span.parent.parent.get_text():
            city = span.get_text()
        elif "State" in span.parent.parent.get_text():
            state = span.get_text()
        elif "Country" in span.parent.parent.get_text(): #there might be an empty line in between
            if len(span.get_text())==0:
                country = span.find_next_sibling().get_text()
        elif "ZIP" in span.parent.parent.get_text():
            zip = span.get_text()
        elif "Normal business" in span.parent.parent.get_text():
            hour =span.get_text()
        elif "Telephone number" in span.parent.parent.get_text():
            telephone_num = span.get_text()
        elif "Facsimile number" in span.parent.parent.get_text():
            facsimile_num = span.get_text()

    data.append(address1)
    data.append(address2)
    data.append(city)
    data.append(state)
    data.append(country)
    data.append(zip)

    imgs = address_table.find_all('img')
    private_residence = 0;
    if not "not" in imgs[0]['alt']:
        private_residence = 1
    data.append(private_residence)

    business_day = 1
    if "not" in imgs[1]:
        business_day = 0
    data.append(business_day)

    data.append(hours)
    data.append(telephone_num)
    data.append(facsimile_num)


    #this part need to be tested
    mail_address1 = ""
    mail_address2 = ""
    mail_city =""
    mail_state=""
    mail_country=""
    mail_zip=""

    mail_address_table = sub_tables[1]
    mail_spans = mail_address_table.find_all("span")

    for span in mail_spans:
        if "Number and Street 1" in span.parent.parent.get_text():
            mail_address1 = span.get_text()
        elif "Number and Street 2" in span.parent.parent.get_text():
            mail_address2 = span.get_text()
        elif "City" in span.parent.parent.get_text():
            mail_city = span.get_text()
        elif "State" in span.parent.parent.get_text():
            mail_state = span.get_text()
        elif "Country" in span.parent.parent.get_text(): #there might be an empty line in between
            if len(span.get_text())==0:
                mail_country = span.find_next_sibling().get_text()
            else:
                mail_country = span.get_text()
        elif "ZIP" in span.parent.parent.get_text():
            mail_zip = span.get_text()


    data.append(mail_address1)
    data.append(mail_address2)
    data.append(mail_city)
    data.append(mail_state)
    data.append(mail_country)
    data.append(mail_zip)

    sole_address1 = ""
    sole_address2 = ""
    sole_city =""
    sole_state=""
    sole_country=""
    sole_zip=""

    data.append(sole_address1)
    data.append(sole_address2)
    data.append(sole_city)
    data.append(sole_state)
    data.append(sole_country)
    data.append(sole_zip)

    web_td = table.find("td",text="I.")
    web_img = web_td.parent.find("img")
    have_website = 1
    if "not" in web_img['alt']:
        have_website = 0
    data.append(have_website)

    #the CCO table
    CCO_table = sub_tables[3]
    cco_span = CCO_table.find_all("span")

    cco_name = ""
    cco_other_titles = ""
    cco_telephone = ""
    cco_facsimile = ""
    cco_address1 = ""
    cco_address2 = ""
    cco_city = ""
    cco_state = ""
    cco_country=""
    cco_zip = ""
    cco_email = ""

    for span in cco_span:
        if "Name" in span.parent.parent.get_text():
            cco_name = span.get_text()
        elif "Other titles" in span.parent.parent.get_text():
            cco_other_titles = span.get_text()
        elif "Telephone number" in span.parent.parent.get_text():
            cco_telephone = span.get_text()
        elif "Facsimile number" in span.parent.parent.get_text():
            cco_facsimile = span.get_text()
        elif "Number and Street 1" in span.parent.parent.get_text():
            cco_address1 = span.get_text()
        elif "Number and Street 2" in span.parent.parent.get_text():
            cco_address2 = span.get_text()
        elif "City" in span.parent.parent.get_text():
            cco_city = span.get_text()
        elif "State" in span.parent.parent.get_text():
            cco_state = span.get_text()
        elif "Country" in span.parent.parent.get_text(): #there might be an empty line in between
            if len(span.get_text())==0:
                cco_country = span.find_next_sibling().get_text()
            else:
                cco_country = span.get_text()
        elif "ZIP" in span.parent.parent.get_text():
            cco_zip = span.get_text()

    data.append(cco_name)
    data.append(cco_other_titles)
    data.append(cco_telephone)
    data.append(cco_facsimile)
    data.append(cco_address1)
    data.append(cco_address2)
    data.append(cco_city)
    data.append(cco_state)
    data.append(cco_country)
    data.append(cco_zip)
    data.append(cco_email)


    arcp_table = sub_tables[4]
    arcp_span = arcp_table.find_all("span")

    arcp_name = ""
    arcp_title = ""
    arcp_telephone = ""
    arcp_facsimile = ""
    arcp_address1 = ""
    arcp_address2 = ""
    arcp_city = ""
    arcp_state = ""
    arcp_country = ""
    arcp_zip = ""
    arcp_mail = ""

    for span in arcp_span:
        if "Name" in span.parent.parent.get_text():
            arcp_name = span.get_text()
        elif "Titles" in span.parent.parent.get_text():
            arcp_title = span.get_text()
        elif "Telephone number" in span.parent.parent.get_text():
            arcp_telephone = span.get_text()
        elif "Facsimile number" in span.parent.parent.get_text():
            arcp_facsimile = span.get_text()
        elif "Number and Street 1" in span.parent.parent.get_text():
            arcp_address1 = span.get_text()
        elif "Number and Street 2" in span.parent.parent.get_text():
            arcp_address2 = span.get_text()
        elif "City" in span.parent.parent.get_text():
            arcp_city = span.get_text()
        elif "State" in span.parent.parent.get_text():
            arcp_state = span.get_text()
        elif "Country" in span.parent.parent.get_text(): #there might be an empty line in between
            if len(span.get_text())==0:
                arcp_country = span.find_next_sibling().get_text()
            else:
                arcp_country = span.get_text();
        elif "ZIP" in span.parent.parent.get_text():
            arcp_zip = span.get_text()
        elif "Electronic mail" in span.parent.parent.get_text():
            arcp_mail = span.get_text()

    data.append(arcp_name)
    data.append(arcp_title)
    data.append(arcp_telephone)
    data.append(arcp_facsimile)
    data.append(arcp_address1)
    data.append(arcp_address2)
    data.append(arcp_city)
    data.append(arcp_state)
    data.append(arcp_country)
    data.append(arcp_zip)
    data.append(arcp_mail)

    l_td = table.find("td",text="L.")
    l_img = l_td.parent.find("img")
    l = 1
    if "not" in l_img['alt']:
        l=0
    data.append(l)

    m_td = table.find("td",text="M.")
    m_img = m_td.parent.find("img")
    m = 1
    if "not" in m_img['alt']:
        m=0
    data.append(m)

    n_td = table.find("td",text="N.")
    n_img = n_td.parent.find("img")
    n = 1
    if "not" in n_img['alt']:
        n=0
    data.append(n)

    cik_row = n_td.parent.find_next_sibling()
    cik_num= cik_row.find("span").get_text()
    data.append(cik_num)

    o_td = table.find("td",text="O.")
    o_img = o_td.parent.find("img")
    o = 1
    if "not" in o_img['alt']:
        o=0
    data.append(o)

    p_td = table.find("td",text="P.")
    p_span = p_td.parent.find("span").get_text()
    data.append(p_span)

    return data


def extract_second_page(file):
    data = []
    soup = BeautifulSoup(file)
    imgs = soup.find_all("img")
    for img in imgs:
        if img.has_attr('alt'):
            if "Checkbox checked" in img['alt']:
                print img['alt']
                if "(" in img.parent.find_next("td").get_text():
                    checked_index = img.parent.find_next("td").get_text()
                elif "Alabama" in img['alt']:
                    print img
                elif "Alaska" in img['alt']:
                    print img
                elif "Arizona" in img['alt']:
                    print img
                elif "Arkansas" in img['alt']:
                    print img
                elif "California" in img['alt']:
                    print img
                elif "Colorado" in img['alt']:
                    print img
                elif "Connecticut" in img['alt']:
                    print img
                elif "Delaware" in img['alt']:
                    print img
                elif "District of Columbia" in img['alt']:
                    print img
                elif "Florida" in img['alt']:
                    print img
                elif "Georgia" in img['alt']:
                    print img
                elif "Guam" in img['alt']:
                    print img
                elif "Hawaii" in img['alt']:
                    print img
                elif "Idaho" in img['alt']:
                    print img
                elif "Illinois" in img['alt']:
                    print img
                elif "Indiana" in img['alt']:
                    print img
                elif "Kansas" in img['alt']:
                    print img
                elif "Kentucky" in img['alt']:
                    print img
                elif "Louisiana" in img['alt']:
                    print img
                elif "Maine" in img['alt']:
                    print img
                elif "Maryland" in img['alt']:
                    print img
                elif "Massachusetts" in img['alt']:
                    print img
                elif "Michigan" in img['alt']:
                    print img
                elif "Minnesota" in img['alt']:
                    print img
                elif "Mississippi" in img['alt']:
                    print img
                elif "Missouri" in img['alt']:
                    print img
                elif "Montana" in img['alt']:
                    print img
                elif "Nebraska" in img['alt']:
                    print img
                elif "Nevada" in img['alt']:
                    print img
                elif "New Hampshire" in img['alt']:
                    print img
                elif "New Jersey" in img['alt']:
                    print img
                elif "New Mexico" in img['alt']:
                    print img
                elif "New York" in img['alt']:
                    print img
                elif "North Carolina" in img['alt']:
                    print img
                elif "North Dakota" in img['alt']:
                    print img
                elif "Ohio" in img['alt']:
                    print img
                elif "Oklahoma" in img['alt']:
                    print img
                elif "Oregon" in img['alt']:
                    print img
                elif "Pennsylvania" in img['alt']:
                    print img
                elif "Puerto Rico" in img['alt']:
                    print img
                elif "Rhode Island" in img['alt']:
                    print img
                elif "South Carolina" in img['alt']:
                    print img
                elif "South Dakota" in img['alt']:
                    print img
                elif "Tennessee" in img['alt']:
                    print img
                elif "Texas" in img['alt']:
                    print img
                elif "Utah" in img['alt']:
                    print img
                elif "Vermont" in img['alt']:
                    print img
                elif "Virgin Islands" in img['alt']:
                    print img
                elif "Virginia" in img['alt']:
                    print img
                elif "Washington" in img['alt']:
                    print img
                elif "West Virginia" in img['alt']:
                    print img
                elif "Wisconsin" in img['alt']:
                    print img

    return data

def extract_third_page(file):
    soup = BeautifulSoup(file)
    imgs = soup.find_all("img")
    for img in imgs:
        if img.has_attr('alt'):
            if "Radio button selected" in img['alt']:
                td = img.parent.find_next("td")
    spans = soup.find_all("span",{'class':"PrintHistRed"})
    month = spans[0].get_text()
    state = spans[1].get_text()
    country = spans[2].get_text()

def extract_fourth_page(file):
    soup = BeautifulSoup(file)
    imgs = soup.find_all("img")
    radioButtons = []
    for img in imgs:
        if img.has_attr("alt"):
            if "Radio button" in img['alt']:
                radioButtons.append(img)
    yes = radioButtons[0]
    no = radioButtons[1]

    span =  soup.find("span",{'class':"IAFormDataValue"})
    data_of_succession = span.get_text()
    print data_of_succession
