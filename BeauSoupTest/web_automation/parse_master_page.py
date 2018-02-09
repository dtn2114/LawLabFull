__author__ = 'yutingchen'

import csv
from global_setting_parsing import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
import xlrd
from iapd import *
import os
import menu
import util
from parse_schedules import *
from parse_DRP import *
import filecmp


import codecs

def initialize_csv(filename):
    """ create a new csv file and write an appropriate column header
    """

    col_header = [["REV_DATE","ORGANIZATION CRD#","FILING TYPE","FULL LEGAL NAME(1A)","PRIMARY BUSINESS NAME(1B)",\
                      "LEGAL NAME CHANGE?(1C)","SEC#(1D)","CRD#(1E)","MAIN OFFICE STREET ADDRESS 1(1F)","MAIN OFFICE STREET ADDRESS2(1F)",\
                    "MAIN OFFICE CITY(1F)","MAIN OFFICE STATE(1F)","MAIN OFFICE COUNTRY(1F)","MAIN OFFICE POSTAL CODE(1F)","PRIVATE RESIDENCE(1F)",\
                    "DAYS OF WEEK WORKED(1F(2))","NORMAL BUSINESS HOURS91F(2))","MAIN OFFICE TELEPHONE NUMBER(1F(3))","MAIN OFFICE FACSIMILE NUMBER(AF(4))",\
                    "MAIL ADDRESS NUMBER AND STREET1(1G)","MAIL ADDRESS NUMBER AND STREET2(1G)","MAIL ADDRESS CITY(1G)","MAIL ADDRESS STATE(1G)",\
                    "MAIL ADDRESS COUNTRY(1G)","MAIL ADDRESS POSTAL CODE(1G)","SOLE PROPRIETOR NUMBER AND STREET1(1H)","SOLE PROPRIETOR NUMBER AND STREET2(1H)",\
                    "SOLE PROPRIETOR CITY(1H)","SOLE PROPRIETOR STATE(1H","SOLE PROPRIETOR COUNTRY(1H)","SOLE PROPRIETOR POSTAL CODE(1H)","WEBSITE(1I)",\
                    "CCO NAME(1J)","CCO OTHER TITLES(1J)","CCO TELEPHONE#(1J)","CCO FACSIMILE#(1J)","CCO NUMBER AND STREET1(1J)","CCO NUMBER AND STREET2(1J)",\
                    "CCO CITY(1J)","CCO STATE(1J)","CCO COUNTRY(1J)","CCO ZIP CODE(1J)","CCO EMAIL(1J)","ARCP NAME(1K)","ARCP TITLES(1K)","ARCP TELEPHONE#(1K)",\
                    "ARCP FACSIMILE#(1K)","ARCP NUMBER AND STREET1(1K)","ARCP NUMBER AND STREET2(1K)","ARCP CITY(1K)","ARCP STATE(1K)","ARCP COUNTRY(1K)",\
                    "ARCP POSTAL CODE(1K)","ARCP EMAIL ADDRESS(1K)","1L","1M","1N","CIK#","1O","1P","AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","GU","HI","ID","IL","IN","IA","KS","KY","LA",\
                    "ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","PR","RI","SC","SD","TN","TX","UT","VT","VI","VA","WA","WV","WI","2B(1)","2B(2)","2B(3)",\
                    "3A","3B","3C State","3C Country","4A","4B","5A","5B(1)","5B(2)","5B(3)","5B(4)","5B(5)","5B(6)","5C(1)","5C(1)number","5C(2)","5D(1)a","5D(1)b",\
                    "5D(1)c","5D(1)d","5D(1)e","5D(1)f","5D(1)g","5D(1)h","5D(1)i","5D(1)j","5D(1)k","5D(1)l","5D(1)m","5D(1)m text","5D(2)a","5D(2)b",\
                    "5D(2)c","5D(2)d","5D(2)e","5D(2)f","5D(2)g","5D(2)h","5D(2)i","5D(2)j","5D(2)k","5D(2)l","5D(2)m","5D(2)m text","5E(1)","5E(2)",\
                    "5E(3)","5E(4)","5E(5)","5E(6)","5E(7)","5F(1)","5F(2)a","5F(2)b","5F(2)c","5F(2)d","5F(2)e","5F(2)f",\
                    "5G(1)","5G(2)","5G(3)","5G(4)","5G(5)","5G(6)","5G(7)","5G(8)","5G(9)","5G(10)","5G(11)","5G(12)","5H(0)","5H(1-10)","5H(11-25)","5H(26-50)","5H(51-100)",\
                    "5H(101-250)","5H(251-500)","5H(More than 500)","5H(number)","5I(1)","5I(2)","5J","6A(1)","6A(2)","6A(3)","6A(4)","6A(5)","6A(6)","6A(7)","6A(8)","6A(9)","6A(10)","6A(11)",\
                    "6A(12)","6A(13)","6A(14)","6B(1)","6B(2)","6B(3)","7A(1)","7A(2)","7A(3)","7A(4)","7A(5)","7A(6)","7A(7)","7A(8)","7A(9)","7A(10)","7A(11)","7A(12)",\
                    "7A(13)","7A(14)","7A(15)","7A(16)","7B","8A(1)","8A(2)","8A(3)","8B(1)","8B(2)","8B(3)","8C(1)","8C(2)","8C(3)","8C(4)","8D","8E","8F","8G(1)","8G(2)",\
                    "8H","8I","9A(1)a","9A(1)b","9A(2)a","9A(2)b","9B(1)a","9B(1)b","9B(2)a","9B(2)b","9C(1)","9C(2)","9C(3)","9C(4)","9D(1)","9D(2)","9E","9F","10A","11","11A(1)",\
                    "11A(2)","11B(1)","11B(2)","11C(1)","11C(2)","11C(3)","11C(4)","11C(5)","11D(1)","11D(2)","11D(3)","11D(4)","11D(5)","11E(1)","11E(2)","11E(3)","11E(4)","11F","11G",\
                    "11H(1)a","11H(1)b","11H(1)c","11H(2)","12A","12B(1)","12B(2)","12C(1)","12C(2)"]]
    try:
        outfile = open(filename, "wb")
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_ALL)
        for row in col_header:
            writer.writerow(row)
        outfile.close()
    except:
        raise


def initialize_scheduleA_csv(filename):
    """create csv file for schedule A's """
    col_header = [["FULL LEGAL NAME","DE/EF/IStatus","Data Status Acquired","Ownership Code","Control Person","PR","CRD No. If None: S.S. No. and Date of Brith, IRS Tax No. or Employee Id No."]]
    try:
        outfile = open(filename, "wb")
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_ALL)
        for row in col_header:
            writer.writerow(row)
        outfile.close()
    except:
        raise

def initialize_scheduleB_csv(filename):
    """create csv file for schedule A's """
    col_header = [["FULL LEGAL NAME","DE/EF/I","Entity in Which Interest is Owned","Status","Data Status Acquired MM/YYYY","Ownership Code","Control Person","PR","CRD No. If None: S.S. No. and Date of Brith, IRS Tax No. or Employee Id No."]]
    try:
        outfile = open(filename, "wb")
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_ALL)
        for row in col_header:
            writer.writerow(row)
        outfile.close()
    except:
        raise



def write(data,filename):
    """ write data to a csv file
    """
    outfile = open(filename, "a")
    writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_ALL)
    for row in data:
        u"{0}".format(row)
        try:
            writer.writerow(row)
        except:
            raise
    outfile.close()


def download_master_page():
    url = open("urls.txt","r")

    for line in url:
        print line
        name_and_url = line.split("|||")
        comp_name = name_and_url[0]
        url = name_and_url[1]
        browser = webdriver.Chrome()
        browser.get(url) #load page
        content = browser.page_source.encode('utf-8')
        file = open("files/"+comp_name,"a")
        file.write(content)
        file.close()

        browser.close()
        time.sleep(0.5)
    #browser.get("http://www.adviserinfo.sec.gov/iapd/content/viewform/adv052003/Sections/iapd_AdvAllPages.aspx?ORG_PK=128552&RGLTR_PK=&STATE_CD=&FLNG_PK=03331FB40008012E04B1EF5000C44845056C8CC0&Print=Y") # Load page
    #content = browser.page_source.encode('utf-8')
    #file = open("files/test","a")
    #file.write(content)

    #file.close()
    #time.sleep(0.5)
    #browser.close()

def extract(file,path):
    directory = os.path.abspath(path+"/"+file)
    html_file = open(directory)
    data = []
    soup = BeautifulSoup(html_file)
    tables = soup.find_all('table',{'class':'PaperFormTableData'})

    try:
        if len(tables)==0: #meaning it's an ADV file
            return data
        rev_date = soup.find('span',{'id':'ctl00_ctl00_cphMainContent_ucADVHeader_lblVersion'}).get_text().encode('ascii', 'ignore')
        data.append(rev_date)

        sec_802 = 0 #flag to distinguih between a state corp

        table = tables[0] #the first page table
        primary_name = table.find('span',{'id':PRIMARY_NAME}).get_text().encode('ascii', 'ignore')
        legal_name = table.find('span',{'id':FULL_LEGAL_NAME}).get_text().encode('ascii', 'ignore')
        sec_number = table.find('span',{'id':SEC_NUM}).get_text().encode('ascii', 'ignore')
        if "80" not in sec_number:
            sec_number = table.find('span',{'id':SEC_NUM_EXEMPT}).get_text().encode('ascii', 'ignore')
        crd_number = table.find('span',{'id':CRD_NUM}).get_text().encode('ascii', 'ignore')
        data.append(crd_number)

        filing_types = file.split("_",1)
        type = filing_types[1].strip('.html')
        data.append(type)

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

        if "802-" in sec_number:
            sec_802 = 1 #mark the difference before parsing item 4 and 5
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
                address1 = span.get_text().encode('ascii', 'ignore')
            elif "Number and Street 2" in span.parent.parent.get_text():
                address2 = span.get_text().encode('ascii', 'ignore')
            elif "City" in span.parent.parent.get_text():
                city = span.get_text().encode('ascii', 'ignore')
            elif "State" in span.parent.parent.get_text():
                state = span.get_text().encode('ascii', 'ignore')
            elif "Country" in span.parent.parent.get_text(): #there might be an empty line in between
                if len(span.get_text())==0:
                    country = span.find_next_sibling().get_text().strip("\n").encode('ascii', 'ignore')
            elif "ZIP" in span.parent.parent.get_text():
                zip = span.get_text().encode('ascii', 'ignore')
            elif "Normal business" in span.parent.parent.get_text():
                hour =span.get_text().encode('ascii', 'ignore')
            elif "Telephone number" in span.parent.parent.get_text():
                telephone_num = span.get_text().encode('ascii', 'ignore')
            elif "Facsimile number" in span.parent.parent.get_text():
                facsimile_num = span.get_text().encode('ascii', 'ignore')

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
                mail_address1 = span.get_text().encode('ascii', 'ignore')
            elif "Number and Street 2" in span.parent.parent.get_text():
                mail_address2 = span.get_text().encode('ascii', 'ignore')
            elif "City" in span.parent.parent.get_text():
                mail_city = span.get_text().encode('ascii', 'ignore')
            elif "State" in span.parent.parent.get_text():
                mail_state = span.get_text().encode('ascii', 'ignore')
            elif "Country" in span.parent.parent.get_text(): #there might be an empty line in between
                if len(span.get_text())==0:
                    mail_country = span.find_next_sibling().get_text().encode('ascii', 'ignore')
                else:
                    mail_country = span.get_text().encode('ascii', 'ignore')
            elif "ZIP" in span.parent.parent.get_text():
                mail_zip = span.get_text().encode('ascii', 'ignore')


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
                cco_name = span.get_text().encode('ascii', 'ignore')
            elif "Other titles" in span.parent.parent.get_text():
                cco_other_titles = span.get_text().encode('ascii', 'ignore')
            elif "Telephone number" in span.parent.parent.get_text():
                cco_telephone = span.get_text().encode('ascii', 'ignore')
            elif "Facsimile number" in span.parent.parent.get_text():
                cco_facsimile = span.get_text().encode('ascii', 'ignore')
            elif "Number and Street 1" in span.parent.parent.get_text():
                cco_address1 = span.get_text().encode('ascii', 'ignore')
            elif "Number and Street 2" in span.parent.parent.get_text():
                cco_address2 = span.get_text().encode('ascii', 'ignore')
            elif "City" in span.parent.parent.get_text():
                cco_city = span.get_text().encode('ascii', 'ignore')
            elif "State" in span.parent.parent.get_text():
                cco_state = span.get_text().encode('ascii', 'ignore')
            elif "Country" in span.parent.parent.get_text(): #there might be an empty line in between
                if len(span.get_text())==0:
                    cco_country = span.find_next_sibling().get_text().encode('ascii', 'ignore')
                else:
                    cco_country = span.get_text().encode('ascii', 'ignore')
            elif "ZIP" in span.parent.parent.get_text():
                cco_zip = span.get_text().encode('ascii', 'ignore')

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
                arcp_name = span.get_text().encode('ascii', 'ignore')
            elif "Titles" in span.parent.parent.get_text():
                arcp_title = span.get_text().encode('ascii', 'ignore')
            elif "Telephone number" in span.parent.parent.get_text():
                arcp_telephone = span.get_text().encode('ascii', 'ignore')
            elif "Facsimile number" in span.parent.parent.get_text():
                arcp_facsimile = span.get_text().encode('ascii', 'ignore')
            elif "Number and Street 1" in span.parent.parent.get_text():
                arcp_address1 = span.get_text().encode('ascii', 'ignore')
            elif "Number and Street 2" in span.parent.parent.get_text():
                arcp_address2 = span.get_text().encode('ascii', 'ignore')
            elif "City" in span.parent.parent.get_text():
                arcp_city = span.get_text().encode('ascii', 'ignore')
            elif "State" in span.parent.parent.get_text():
                arcp_state = span.get_text().encode('ascii', 'ignore')
            elif "Country" in span.parent.parent.get_text(): #there might be an empty line in between
                if len(span.get_text())==0:
                    arcp_country = span.find_next_sibling().get_text().encode('ascii', 'ignore')
                else:
                    arcp_country = span.get_text().encode('ascii', 'ignore')
            elif "ZIP" in span.parent.parent.get_text():
                arcp_zip = span.get_text().encode('ascii', 'ignore')
            elif "Electronic mail" in span.parent.parent.get_text():
                arcp_mail = span.get_text().encode('ascii', 'ignore')

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
        cik_num= cik_row.find("span").get_text().encode('ascii', 'ignore')
        data.append(cik_num)

        o_td = table.find("td",text="O.")
        o_img = o_td.parent.find("img")
        o = 1
        if "not" in o_img['alt']:
            o=0
        data.append(o)

        p_td = table.find("td",text="P.")
        p_span = p_td.parent.find("span").get_text().encode('ascii', 'ignore')
        data.append(p_span)
        data = extract_second_third_page(data,tables,sec_802,soup)
        data = extract_fourth_fifth_page(data,tables,sec_802,soup)

    except:
        print "error:"+file

    print data
    return data

def extract_second_third_page(data,tables,sec_802,soup):
    if sec_802 ==0:
        second_page_result = soup.find("tr",{'id':ITEM2})
        if second_page_result == None:
            for i in range(0,53):
                data.append("N/A")
        else:
            #second_page = tables[1]
            second_page = second_page_result.parent
            imgs = second_page.find_all("img")
            for img in imgs:
                if img.has_attr('alt'):
                    if "Checkbox" in img['alt'] and "checked" in img['alt']:
                        if "(" in img.parent.find_next("td").get_text():
                            checked_index = img.parent.find_next("td").get_text()
                        elif "Alabama" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Alaska" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Arizona" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Arkansas" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "California" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Colorado" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Connecticut" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Delaware" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "District of  Columbia" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Florida" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Georgia" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Guam" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Hawaii" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Idaho" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Illinois" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Indiana" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Iowa" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Kansas" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Kentucky" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Louisiana" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Maine" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Maryland" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Massachusetts" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Michigan" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Minnesota" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Mississippi" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Missouri" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Montana" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Nebraska" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Nevada" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "New Hampshire" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "New Jersey" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "New Mexico" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "New York" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "North Carolina" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "North Dakota" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Ohio" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Oklahoma" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Oregon" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Pennsylvania" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Puerto Rico" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Rhode Island" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "South Carolina" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "South Dakota" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Tennessee" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Texas" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Utah" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Vermont" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Virgin Islands" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Virginia" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Washington" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "West Virginia" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)
                        elif "Wisconsin" in img['alt']:
                            if "not" in img['alt']:
                                data.append(0)
                            else:
                                data.append(1)

        data.append("N/A") #data entry only available for state filed SEC
        data.append("N/A")
        data.append("N/A")

        third_page = soup.find("tr",{'id':ITEM3}).parent
        #third_page = tables[2]
        imgs = third_page.find_all("img")
        for img in imgs:
            if img.has_attr('alt'):
                if "Radio button selected" in img['alt']:
                    td = img.parent.find_next("td")
                    #print td.get_text().strip("\n")
                    data.append(td.get_text().encode("utf-8").strip().strip("\n"))
        spans = third_page.find_all("span",{'class':"PrintHistRed"})
        try:
            month = spans[0].get_text().encode("utf-8")
            state = spans[1].get_text().encode("utf-8")
            country = spans[2].get_text().encode("utf-8")
            data.append(month)
            data.append(state)
            data.append(country)
        except:
            month = spans[0].get_text().encode("utf-8")
            state_country = spans[1].get_text().encode("utf-8")
            data.append(month)
            data.append(state_country)
            data.append(state_country)
    else:
        for i in range(0,53):
            data.append("N/A")
        item_tables = soup.find_all('table',{'class':'flatBorderTable'})
        second_page = item_tables[1]
        imgs = second_page.find_all("img")
        for img in imgs:
            if "not" in img['alt']:
                data.append(0)
            else:
                data.append(1)

        third_page = soup.find("tr",{'id':ITEM3}).parent
        imgs = third_page.find_all("img")
        for img in imgs:
            if img.has_attr('alt'):
                if "Radio button selected" in img['alt']:
                    td = img.parent.find_next("td")
                    texts = td.get_text().split("(specify):")
                    #print texts[1].encode("utf-8").lstrip().strip("\n")
                    data.append(texts[1].encode("utf-8").lstrip().strip("\n"))
        spans = third_page.find_all("span",{'class':"PrintHistRed"})
        month = spans[0].get_text().encode("utf-8")
        state = spans[1].get_text().encode("utf-8")
        country = spans[2].get_text().encode("utf-8")
        data.append(month)
        data.append(state)
        data.append(country)

    return data

def extract_fourth_fifth_page(data,tables,sec_802,soup):
    if sec_802 ==0:
        fourth_page = soup.find("tr",{'id':ITEM4}).parent
        #fourth_page = tables[3]
        imgs = fourth_page.find_all("img")
        radioButtons = []
        for img in imgs:
            if img.has_attr("alt"):
                if "Radio button" or "Checkbox" in img['alt']:
                    radioButtons.append(img)
        yes = radioButtons[0]
        if "not" in yes['alt']:
            data.append(0)
        else:
            data.append(1)

        span =  fourth_page.find("span",{'class':"IAFormDataValue"})
        data_of_succession = span.get_text()
        data.append(data_of_succession)

        fifth_table = soup.find("tr",{'id':ITEM5}).parent
        fifth_page = fifth_table.find("table",{'class':"PaperFormTableData"})
        #fifth_page = tables[4]
        spans = fifth_page.find_all("span")

        item_5a = spans[0].get_text().encode('ascii', 'ignore')
        item_5b1 = spans[1].get_text().encode('ascii', 'ignore')
        item_5b2 = spans[2].get_text().encode('ascii', 'ignore')
        item_5b3 = spans[3].get_text().encode('ascii', 'ignore')
        item_5b4 = spans[4].get_text().encode('ascii', 'ignore')
        item_5b5 = spans[5].get_text().encode('ascii', 'ignore')
        item_5b6 = spans[6].get_text().encode('ascii', 'ignore')

        data.append(item_5a)
        data.append(item_5b1)
        data.append(item_5b2)
        data.append(item_5b3)
        data.append(item_5b4)
        data.append(item_5b5)
        data.append(item_5b6)


        imgs = fifth_page.find_all("img")
        for i in range(0,5):
            if "not" not in imgs[i]['alt']:
                value  = imgs[i].get_text().encode('ascii', 'ignore')
                if "More than 100" in value:
                        data.append("More than 100")
                        #if more than 100, find the span and print the number
                        value_text = value.split("(round to the nearest 100)")
                        value_text = value_text[1].encode('ascii', 'ignore').strip()
                        data.append(value_text)
                else:
                    values = value.split("\r")
                    clean_values = values[0].split("\n")
                    data.append(clean_values[0])
                    data.append("")

                item_5c2 = spans[8].get_text().encode('ascii', 'ignore')
                data.append(item_5c2)

        for j in range(5,96):
            index_adjust = 4
            if "not" not in imgs[j]['alt']:
                remainder = (j-index_adjust)%7
                if remainder == 1:
                    data.append("None")
                elif remainder ==2:
                    data.append("10%")
                elif remainder ==3:
                    data.append("11-25%")
                elif remainder ==4:
                    data.append("26-50%")
                elif remainder ==5:
                    data.append("51-75%")
                elif remainder ==6:
                    data.append("76-99%")
                elif remainder ==0:
                    data.append("100%")

        #need to check if the (m)other row has any chosen options
        has_other_choices = False
        for m in range (89,96):
            if "not" not in imgs[m]['alt']:
                has_other_choices = True
                break
        if not has_other_choices:
            data.append("N/A")

        item_5d1m = spans[9].get_text().encode('ascii', 'ignore')
        data.append(item_5d1m)

        for k in range(96,96+5*13):
            index_adjust2 = 95
            if "not" not in imgs[k]['alt']:
                remainder = (k-index_adjust2)%5
                if remainder == 1:
                    data.append("None")
                elif remainder ==2:
                    data.append("25%")
                elif remainder ==3:
                    data.append("50%")
                elif remainder ==4:
                    data.append("75%")
                elif remainder ==0:
                    data.append(">75%")

        #need to check if the (m)other row has any chosen options
        has_2m_choices = False
        for z in range (96+5*12,96+5*13):
            if "not" not in imgs[z]['alt']:
                has_2m_choices = True
                break
        if not has_2m_choices:
            data.append("N/A")

        item_5d2m = spans[10].get_text().encode('ascii', 'ignore')
        data.append(item_5d2m)

        for l in range(0,7):
            index = len(imgs)-7+l
            if "not" not in imgs[index]['alt']:
                data.append(1)
            else:
                data.append(0)

        """

        tds = fifth_page.find_all("td")
        for td in tds:
            if td.get_text().encode('utf-8')=="(1)":
                partc_table = td.parent.find_next("tr").find_next("table")
                imgs = partc_table.find_all("img")
                for img in imgs:
                    print img
                    if "not" not in img['alt']:
                        value = img.get_text()
                        if "More than 100" in value:
                            data.append("More than 100")
                             #if more than 100, find the span and print the number
                            value2 = partc_table.find("span")
                            data.append(value2.get_text())
                        else:
                            data.append(value)
                            data.append()

                break

            ######Mark this as wrong #############################
            if td.get_text().encode('utf-8')=="(2)":
                #print td.find_next("td").get_text() #still not correct

                span = td.parent.find_next("tr").find("span")
               # print span.get_text()
               # data.append(span.get_text())
                break
        """

        #item5_f = tables[5]
        item5_f_page = soup.find("tr",{'id':ITEM5_F}).parent
        radio = item5_f_page.find("img") #get the value of the first radio button
        if "not" in img['alt']:
            data.append(0)
        else:
            data.append(1)

        item5_f = item5_f_page.find("table",{'class':'PaperFormTableData'})
        spans = item5_f.find_all("span")
        item5_f2a = spans[0].get_text().encode('ascii', 'ignore')
        item5_f2b = spans[2].get_text().encode('ascii', 'ignore')
        item5_f2c = spans[4].get_text().encode('ascii', 'ignore')
        item5_f2d = spans[1].get_text().encode('ascii', 'ignore')
        item5_f2e = spans[3].get_text().encode('ascii', 'ignore')
        item5_f2f = spans[5].get_text().encode('ascii', 'ignore')
        data.append(item5_f2a)
        data.append(item5_f2b)
        data.append(item5_f2c)
        data.append(item5_f2d)
        data.append(item5_f2e)
        data.append(item5_f2f)


        item5_g = soup.find("tr",{'id':ITEM5_G}).parent
        #item5_g = tables[6]
        imgs = item5_g.find_all("img")
        for i in range(0,len(imgs)-1): #does not have to count the last one since it's radio button
            if "not" in imgs[i]['alt']:
                data.append(0)
            else:
                data.append(1)

        item5h_number_span = item5_g.find("span")
        item5h_number = item5h_number_span.get_text().encode('ascii', 'ignore')
        data.append(item5h_number)
    else:
        for i in range(0,78):
            data.append("N/A")

    return extract_sixth_seventh_page(data,tables,sec_802,soup)

def extract_sixth_seventh_page(data,tables,sec_802,soup):
    if sec_802 == 0:
        item6 =soup.find('tr',{'id':ITEM6}).parent
        imgs = item6.find_all("img")
        for i in range(0,14):
            if "not" in imgs[i]['alt']:
                data.append(0)
            else:
                data.append(1)

        #check whether the first radio button is selected in the radio button group in each row
        count = 0;
        for j in range(14,len(imgs)):
            if count%2==0:
                if "not" in imgs[j]['alt']:
                    data.append(0)
                else:
                    data.append(1)
            count = count+1

        item7 =soup.find('tr',{'id':ITEM7}).parent
        imgs = item7.find_all("img")

        for i in range(0,16):
            if "not" in imgs[i]['alt']:
                data.append(0)
            else:
                data.append(1)

        count = 0;
        for j in range(16,len(imgs)):
            if count%2==0:
                if "not" in imgs[j]['alt']:
                    data.append(0)
                else:
                    data.append(1)
            count = count+1
    else:
        item6 = soup.find('tr',{'id':ITEM6}).parent
        imgs = item6.find_all("img")
        for i in range(0,14):
            if "not" in imgs[i]['alt']:
                data.append(0)
            else:
                data.append(1)

        #check whether the first radio button is selected in the radio button group in each row
        count = 0;
        for j in range(14,len(imgs)):
            if count%2==0:
                if "not" in imgs[j]['alt']:
                    data.append(0)
                else:
                    data.append(1)
            count = count+1


        item7  = soup.find('tr',{'id':ITEM7}).parent
        imgs = item7.find_all("img")

        for i in range(0,16):
            if "not" in imgs[i]['alt']:
                data.append(0)
            else:
                data.append(1)

        count = 0;
        for j in range(16,len(imgs)):
            if count%2==0:
                if "not" in imgs[j]['alt']:
                    data.append(0)
                else:
                    data.append(1)
            count = count+1

    return extract_eighth_ninth_page(data,tables,sec_802,soup)

def extract_eighth_ninth_page(data,tables,sec_802,soup):
    if sec_802 == 0:
        item8_page = soup.find("tr",{'id':ITEM8}).parent
        item8 = item8_page.find("table",{'class':'PaperFormTableData'})
        #item8 = tables[9]
        imgs = item8.find_all("img")
        count = 0
        for img in imgs:
            if count %2 ==0:
                if "not" in img['alt']:
                    data.append(0)
                else:
                    data.append(1)
            count = count +1

        item9_page = soup.find("tr",{'id':ITEM9}).parent
        #item9 = tables[10]
        item9 = item9_page.find("table",{'class':'PaperFormTableData'})
        imgs = item9.find_all("img")
        if "not" in imgs[0]['alt']:
            data.append(0)
        else:
            data.append(1)

        if "not" in imgs[2]['alt']:  #check the first radio button in the first two groups
            data.append(0)
        else:
            data.append(1)
        spans = item9.find_all("span")
        item9_a2a = spans[0].get_text().encode('ascii', 'ignore')
        item9_a2b = spans[1].get_text().encode('ascii', 'ignore')
        data.append(item9_a2a)
        data.append(item9_a2b)

        if "not" in imgs[4]['alt']:
            data.append(0)
        else:
            data.append(1)

        if "not" in imgs[6]['alt']:
            data.append(0)
        else:
            data.append(1)

        item9_b2a = spans[2].get_text().encode('ascii', 'ignore')
        item9_b2b = spans[3].get_text().encode('ascii', 'ignore')
        data.append(item9_b2a)
        data.append(item9_b2b)

        for j in range(8,12):
            if "not" in imgs[j]["alt"]:
                data.append(0)
            else:
                data.append(1)

        if "not" in imgs[12]['alt']:
            data.append(0)
        else:
            data.append(1)
        if "not" in imgs[14]['alt']:
            data.append(0)
        else:
            data.append(1)
        item9_e = spans[5].get_text().encode('ascii', 'ignore')
        item9_f = spans[6].get_text().encode('ascii', 'ignore')
        data.append(item9_e)
        data.append(item9_f)
    else:
        for i in range(0,33):
            data.append("N/A")

    return extract_tenth_eleventh_page(data,tables,sec_802,soup)

def extract_tenth_eleventh_page(data,tables,sec_802,soup):
    if sec_802 ==0:
        item10 = soup.find("tr",{'id':ITEM10}).parent
        #item10 = tables[11] #only need to check if the first "yes" option is checked
        imgs = item10.find("img")
        if "not" in imgs['alt']:
            data.append(0)
        else:
            data.append(1)

        item11_page = soup.find("tr",{'id':ITEM11}).parent
        item11_tables=  item11_page.find_all('table',{'class':'PaperFormTableData'})
        item11_part1 = item11_tables[0]


        img = item11_part1.find("img")#only need to check if the first "yes" option is checked

        if "not" in img['alt']:
            data.append(0)
        else:
            data.append(1)

        item11_part2 = item11_tables[1]
        #only need to check the even number checkboxes as #0,#2,#4..etc
        imgs = item11_part2.find_all("img")
        count = 0;
        for img in imgs:
            if count%2==0:
                if "not" in img['alt']:
                    data.append(0)
                else:
                    data.append(1)
            count = count+1

        item11_part3 = item11_tables[2]
        #only need to check the even number checkboxes as #0,#2,#4..etc
        imgs = item11_part3.find_all("img")
        count = 0;
        for img in imgs:
            if count%2==0:
                if "not" in img['alt']:
                    data.append(0)
                else:
                    data.append(1)
            count = count+1

        item11_part4 = item11_tables[3]
        #only need to check the even number checkboxes as #0,#2,#4..etc
        imgs = item11_part4.find_all("img")
        count = 0;
        for img in imgs:
            if count%2==0:
                if "not" in img['alt']:
                    data.append(0)
                else:
                    data.append(1)
            count = count+1
    else:
        item10 = soup.find("tr",{'id':ITEM10}).parent #only need to check if the first "yes" option is checked

        imgs = item10.find("img")
        if "not" in imgs['alt']:
            data.append(0)
        else:
            data.append(1)

        item11_page = soup.find("tr",{'id':ITEM11}).parent
        item11_tables= item11_page.find_all('table',{'class':'PaperFormTableData'})
        item11_part1 = item11_tables[0]

        img = item11_part1.find("img")#only need to check if the first "yes" option is checked

        if "not" in img['alt']:
            data.append(0)
        else:
            data.append(1)

        item11_part2 = item11_tables[1]
        #only need to check the even number checkboxes as #0,#2,#4..etc
        imgs = item11_part2.find_all("img")
        count = 0;
        for img in imgs:
            if count%2==0:
                if "not" in img['alt']:
                    data.append(0)
                else:
                    data.append(1)
            count = count+1

        item11_part3 = item11_tables[2]
        #only need to check the even number checkboxes as #0,#2,#4..etc
        imgs = item11_part3.find_all("img")
        count = 0;
        for img in imgs:
            if count%2==0:
                if "not" in img['alt']:
                    data.append(0)
                else:
                    data.append(1)
            count = count+1

        item11_part4 = item11_tables[3]
        #only need to check the even number checkboxes as #0,#2,#4..etc
        imgs = item11_part4.find_all("img")
        count = 0;
        for img in imgs:
            if count%2==0:
                if "not" in img['alt']:
                    data.append(0)
                else:
                    data.append(1)
            count = count+1

    return extract_twelvth_page(data,tables,sec_802,soup)

def extract_twelvth_page(data,tables,sec_802,soup):
     item12_table = soup.find("tr",{'id':ITEM12})
     if item12_table!= None:
         item12=  item12_table.parent
         imgs = item12.find_all("img")
         for i in range(0,5):
             if "not" not in imgs[2*i]['alt']:
                 data.append("1")
             else:
                 if "not" not in imgs[2*i+1]['alt']:
                     data.append("0")
                 else:
                     data.append("no answer")
     else:
         for i in range(0,5):
            data.append("N/A")
     return data

def extract_ScheduleA(file,comp_crd,comp_name):
    data = []
    soup = BeautifulSoup(open(file))
    part2 = soup.find('table',{'id':PART2})
    if part2!=None:
        scheduleA_sec = part2.find_next("table")

        comp_row = []
        comp_row.append(comp_crd)
        comp_row.append(comp_name)
        '''if scheduleA_sec!=None:
            img = scheduleA_sec.find("img")
            if "not" not in img['alt']:
                comp_row.append("Have indirect owners")
            else:
                comp_row.append("Does not have indirect owners")'''
        for j in range(0,6):
            comp_row.append("")

        data.append(comp_row)

        scheduleA_table = soup.find('table',{'id':SCHEDULE_A})
        if scheduleA_table != None:

            trs = scheduleA_table.find_all('tr')
            for i in range(1,len(trs)):
                row = []
                tds = trs[i].find_all('td')
                for td in tds:
                    #print td.get_text()
                    row.append((td.get_text()).strip('\n').encode('ascii', 'ignore'))
                data.append(row)
        print data
    return data

def extract_ScheduleB(file,comp_crd,comp_name):
    data = []
    soup = BeautifulSoup(open(file))
    scheduleB_table = soup.find('table',{'id':SCHEDULE_B_TABLE})
    if scheduleB_table!=None:
        comp_row = []
        comp_row.append(comp_crd)
        comp_row.append(comp_name)
        for j in range(0,7):
            comp_row.append("")
        data.append(comp_row)
        trs = scheduleB_table.find_all('tr')
        for i in range(1,len(trs)):
            row = []
            tds = trs[i].find_all('td')
            for td in tds:
                #print td.get_text()
                row.append((td.get_text()).strip('\n').encode('ascii', 'ignore'))
            data.append(row)
    print data
    return data

def get_crds_from_file(file):
    excelFile = xlrd.open_workbook(file)
    crds = []
    sheet = excelFile.sheets()[0]
    for row_index in range(1,sheet.nrows):
        row = sheet.row(row_index)
        crds.append(int(row[0].value))
    return crds

def download_files_from_file_input(crds, file_directory):
     for crd in crds:
            iapd = Iapd(int(crd))
            iapd.download_combined(os.path.abspath(os.getcwd()+"/"+file_directory))
            print "Files downloaded into directory "+file_directory


#download the master pages of companies in the crd ranges specified by the user
#is_range indicates if the parameter is crd range or list
def download_files(range_of_crds,is_range):

    input_directory = raw_input(">> Please enter the directory where you want to store the files, default[files/]: ")
    current_time =  datetime.datetime.now()
    current_time = str(current_time).split('.')[0]
    #make a new directory with current_time
    path = process_storage_directory(input_directory)
    file_directory = os.path.abspath(os.getcwd()+"/"+path+"/"+str(current_time)+"/")
    os.mkdir(os.path.abspath(file_directory))

    if is_range:
        valid_crd_range = util.is_valid_crd_range(range_of_crds)
        if valid_crd_range:
            print "File downloading..."
            for i in range(int(valid_crd_range[0]),int(valid_crd_range[1])):
                iapd = Iapd(i)
                iapd.download_combined(file_directory)
            print "Files downloaded into directory "+file_directory
        else:
            print "Input is not valid CRD range"
            range_of_crds = raw_input(">> Please reenter the range of CRD numbers. Eg.[1,10000]:"+"\n"+"If you would like to go back, type Back:")
            if "back" in range_of_crds.lower():
                process_crd_input()
            else:
                download_files(range_of_crds,True)

    else:
        valid_crds = util.is_valid_crds(range_of_crds)
        if valid_crds:
            print "File downloading..."
            for crd in valid_crds:
                iapd = Iapd(int(crd))
                iapd.download_combined(file_directory)
            print "Files downloaded into directory /"+file_directory
        else:
            print "Input is not valid CRDs"
            range_of_crds = raw_input(">> Please reenter one or multiple CRD numbers, separated by comma. Eg. 1,101,306:"+"\n"+"If you would like to go back, type Back:")
            if "back" in range_of_crds.lower():
                process_crd_input()
            else:
                download_files(range_of_crds,False)


def parse_data(path):
    #Find the files directory, loop through all files. If they are not ADV formats, parse them and write the results into the csv
    list_of_data =[]
    output_file_name = raw_input(">> Please enter the name of the output csv file, [default] output.csv.")
    if output_file_name.strip()=="" or len(output_file_name)==0:
        output_file_name = "output"
    try:
        list = os.listdir(path)
        has_html_file = False
        initialize_csv("output/"+output_file_name+".csv")
        initialize_scheduleA_csv("output/scheduleA.csv")
        initialize_scheduleB_csv("output/scheduleB.csv")
        initialize_DRP_csv_part1("output/DRP_part1.csv")
        initialize_DRP_csv_part2("output/DRP_part2.csv")
        initialize_scheduleD()

        for file in list:
            if file.endswith(".html"):
                has_html_file = True
                if "ADV" not in file:
                    data = extract(file,path)
                    list =[]
                    list.append(data)
                    write(list,"output/"+output_file_name+".csv")

                    directory = os.path.abspath(path+"/"+file)
                    #parse scheduleAs as well and write outputs in a seperate file
                    data_scheduleA = extract_ScheduleA(directory,data[0],data[3])
                    if len(data_scheduleA)!=0:
                        write(data_scheduleA,"output/scheduleA.csv")

                    data_scheduleV = extract_ScheduleB(directory,data[0],data[3])
                    if len(data_scheduleV)!=0:
                        write(data_scheduleV,"output/scheduleB.csv")

                    data_DRP_part1 = extract_ScheduleDRP_part1(directory,data[0],data[3])
                    if len(data_DRP_part1)!=0:
                        write(data_DRP_part1,"output/DRP_part1.csv")

                    data_DRP_part2 = extract_ScheduleDRP_part2(directory,data[0],data[3])
                    if len(data_DRP_part2)!=0:
                        write(data_DRP_part2,"output/DRP_part2.csv")

                    write_scheduleD_xlsx(directory,data[3])

        if has_html_file:
            return list_of_data
        else:
            print "Error! File directory is not correct or there is no valid html files in the directory"
            return False
    except OSError,e:
        print e
        downloaded_directory = raw_input(">> Please reenter the directory of downloaded files using absolute path. Eg. user/abc/desktop/iapd_files:")
        downloaded_directory = os.path.abspath(downloaded_directory)
        parse_data(downloaded_directory)


def process_crd_input_file(file):
    #check if the file exists and is readable
    try:
        file_exists = os.path.exists(file)
        if file_exists:
            input_directory = raw_input(">> Please enter the directory where you want to store the files, [default]:"+datetime.datetime.now()+"/")
            file_directory = process_storage_directory(input_directory)
            file_directory = os.path.abspath(file_directory)
            crds = get_crds_from_file(file)
            download_files_from_file_input(crds,file_directory)
        else:
            print "File does not exist."
            crd_file = raw_input(">> Please reenter the directory of the file: ")
            process_crd_input_file(crd_file)
    except OSError,e:
        print e
        crd_file = raw_input(">> Please reenter the directory of the file: ")
        process_crd_input_file(crd_file)

def process_storage_directory(file_directory):
    if file_directory =="" or len(file_directory)==0:
            file_directory = "files"
    else:
        directory = os.path.abspath(os.getcwd()+"/"+file_directory)
        directory_exists = os.path.exists(directory)
        if not directory_exists:
            os.mkdir(directory)
    return file_directory

def process_crd_input():
    menu.display_sub_menu()
    user_selection = util.sub_menu()
    if user_selection =="0":
        menu.display()
    elif user_selection =="1":
        file_input = raw_input(">> Please input the directory of the file: "+"\n"+"If you would like to go back, type Back:")
        if "back" in file_input.lower():
            process_crd_input()
        else:
            file_input = os.path.abspath(file_input)
            valid_name = util.is_valid_filename(file_input)
            if valid_name:
                process_crd_input_file(file_input)
            else:
                file_path = raw_input(">> Please reenter the directory of the file: ")

                process_crd_input_file(file_path)
    elif user_selection =="2":
        range_of_crds = raw_input(">> Please input the range of CRD numbers. Eg.[1,10000]:"+"\n"+"If you would like to go back, type Back:")
        if "back" in range_of_crds.lower():
            process_crd_input()
        else:
            download_files(range_of_crds,True)
    elif user_selection =="3":
        crds = raw_input(">> Please input one or multiple CRD numbers, separated by comma. Eg. 1,101,306:"+"\n"+"If you would like to go back, type Back:")
        if "back" in crds.lower():
            process_crd_input()
        else:
            is_range = False
            download_files(crds,is_range)
    elif user_selection =="4":
        downloaded_directory = raw_input(">> Please input the directory of downloaded files using absolute path. Eg. user/abc/desktop/iapd_files:"+"\n"+"If you would like to go back, type Back:")
        downloaded_directory = os.path.abspath(downloaded_directory)
        print downloaded_directory
        if "back" in downloaded_directory.lower():
            process_crd_input()
        else:
            parse_data(downloaded_directory)

def update_files_directory(path):
    #download all the files again in the new directory with today's date, compare two files and if the file has been updated, keep the new version, otherwise remove the file

    most_recent_directory = util.getLastModifiedDirectory(path)

    current_time =  datetime.datetime.now()
    current_time = str(current_time).split('.')[0]
    #make a new directory with current_time
    current_directory = os.path.abspath(os.getcwd()+"/"+path+"/"+str(current_time)+"/")
    os.mkdir(os.path.abspath(os.getcwd()+"/"+path+"/"+str(current_time)))
    os_path = os.listdir(os.path.abspath(os.getcwd()+"/"+path+"/"+most_recent_directory))
    list_of_crds = []
    for file in os_path:
        if file.endswith(".html"):
            number = filter(str.isdigit, file)
            list_of_crds.append(number)
            #download the file on the SEC into the new folder
    download_files_from_file_input(list_of_crds,os.path.abspath(path+"/"+str(current_time)+"/"))


    recent_file_directory = os.listdir(os.path.abspath(os.getcwd()+"/"+path+"/"+most_recent_directory))
    file1_directory = os.path.abspath(os.getcwd()+"/"+path+"/"+most_recent_directory+"/")

    for file in recent_file_directory:
        file2 = current_directory+file
        #compare files in the most recent directory and directory just downloaded
        same_file = cmp_files(file1_directory+file,file2)
        if same_file:
            os.remove(file2)

def cmp_files(file1, file2):
    return filecmp.cmp(file1, file2, shallow=False)

def check_file_update():
    path = raw_input(">> Please input the directory of previously downloaded files,default[files]:")
    time = util.getLastModifiedDirectory(path)
    if time == None:
        check_file_update()
    print "Files last updated:" + time
    yes_or_no_input = util.get_yes_no("Continue to update?")
    if yes_or_no_input == "Yes":
       files_to_update = raw_input(">> Please input the directory of files you want to update:")
       #menu.display_update_menu()
       #util.sub_menu()
       update_files_directory(files_to_update)
    else:
        print "Back to Main Menu"


def return_to_main_menu():
    return 'main_menu'

def exit_program():
    return 'exit'
    
if __name__ == "__main__":
    initialize_csv("output.csv")
    #crds = get_crds_from_file('20140331CRD.xlsx')
    #download_files(crds)
    #parse_data()


    #data = extract("110353_SEC.html","files/")
    #data = extract("104323_NEW_YORK.html","files/")
    #data = extract("106287_NEW_YORK.html","files/")

    #scheduleB = 157325
    #initialize_scheduleB_csv("scheduleB.csv")
    #data = extract_ScheduleB("files/157325_SEC.html","aurelius","157325")
    #if len(data)!=0:
    #    write(data,"scheduleB.csv")
    #extract_ScheduleDRP_part1('361_drp.html')
    #extract_ScheduleDRP_part1('files/110353_SEC.html')
    #write_DRP_xlsx('drp_example.xls','files/110353_SEC.html')

    #soup = BeautifulSoup(open('361_drp.html'))
    #write_scheduleD("files/110353_SEC.html")
    #initialize_scheduleD()
    #write_scheduleD_xlsx("files/110353_SEC.html","ms")
    #write_scheduleD_xlsx('example.xls',"files/110353_SEC.html")
    #data = extract_ScheduleD("files/157325_SEC.html","aurelius","157325")

    #data = extract_ScheduleD("files/110353_SEC.html","aurelius","157325")

    #update_files_directory('files1/2014-05-07 15:15:07')


    while True:
        menu.display()

        functions = {'0':return_to_main_menu,
                     '1':process_crd_input,
                     '2':check_file_update,
                     '3':exit_program}
        func = functions[util.main_menu()]
        return_code = func()
        if return_code == 'exit':
            break