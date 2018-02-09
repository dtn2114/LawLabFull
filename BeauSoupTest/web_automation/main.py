__author__ = 'yutingchen'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import os
import csv
import time
from global_setting import *
from parsing_pages import *
from iapd import *

def get_company_names(search_keyword):

    soup = BeautifulSoup();
    browser = webdriver.Chrome()
    company_names=[]
    #browser = webdriver.Chrome()
    browser.get("http://www.adviserinfo.sec.gov/IAPD/Content/Search/iapd_Search.aspx") # Load page
    elem = browser.find_element_by_id("ctl00_cphMainContent_ucUnifiedSearch_rdoOrg") # Find the radio button
    elem.click()
    time.sleep(0.1) # Let the page load, will be added to the API

    search_box = browser.find_element_by_name("ctl00$cphMainContent$ucUnifiedSearch$txtFirm")
    search_box.send_keys(search_keyword)
    time.sleep(3)

    #list_box = browser.find_element_by_tag_name("ul")
    try:
        while browser.find_element_by_class_name("s4_more")!= None:
            names = browser.find_elements_by_class_name("s4_item-field")
            last_comp_name = names[len(names)-1].text
            words_in_name = last_comp_name.split()
            #print words_in_name
            if search_keyword in words_in_name[0]:
                more = browser.find_element_by_class_name("s4_more")
                more.click()
                time.sleep(1)
            else:
                content = browser.page_source
                soup = BeautifulSoup(content)
                companys =[]
                divs = soup.find_all("div")

                for div in divs:
                    if div.has_attr("class"):
                        print div['class']
                        if "s4_suggestion" in div['class']:
                            name = div.get_text()
                            names = name.split()
                            if search_keyword in names[0]: #only store names that has keywords in its first word
                                companys.append(div.get_text())
                for company in companys:
                    list = []
                    list.append(company)
                    company_names.append(list)
                print company_names
                return company_names,browser

    except NoSuchElementException:
        content = browser.page_source
        soup = BeautifulSoup(content)
        companys =[]
        divs = soup.find_all("div")

        for div in divs:
            if div.has_attr("class"):
                print div['class']
                if "s4_suggestion" in div['class']:
                    companys.append(div.get_text())

        print companys

        for company in companys:
            list = []
            list.append(company)
            company_names.append(list)
    except:
        print "error"
        content = browser.page_source
        soup = BeautifulSoup(content)
        companys =[]
        divs = soup.find_all("div")

        for div in divs:
            if div.has_attr("class"):
                print div['class']
                if "s4_suggestion" in div['class']:
                    companys.append(div.get_text())

        print companys

        for company in companys:
            list = []
            list.append(company)
            company_names.append(list)
    return company_names,browser
    #time.sleep(1)
    #browser.close()


def initialize_csv(filename):
    """ create a new csv file and write an appropriate column header
    """

    col_header = [["Company Name","CRD#"]]
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
            print row
            pass
    outfile.close()

def find_crd(comp_name,browser):

    search_box = browser.find_element_by_name("ctl00$cphMainContent$ucUnifiedSearch$txtFirm")
    search_box.clear()
    search_box.send_keys(comp_name)
    time.sleep(1)

    try:
        start_button = browser.find_element_by_name("ctl00$cphMainContent$ucUnifiedSearch$btnFreeFormSearch")
        start_button.click()
    except:
        click_item = browser.find_element_by_class_name("s4_suggestion")
        click_item.click()
        time.sleep(0.5)

        start_button = browser.find_element_by_name("ctl00$cphMainContent$ucUnifiedSearch$btnFreeFormSearch")
        start_button.click()

    finally:
        try:
            href = browser.find_element_by_xpath("//*[@title='Link to Form ADV']")
            href.click()
            time.sleep(1)
            crd = ""
            a_tags = browser.find_elements_by_tag_name("a")
            for a in a_tags:
                try:
                    attr = a.get_attribute("href")
                    if attr != None:
                        if "crd_iapd" in attr:
                            a.click()
                            time.sleep(0.5)

                            browser = save_full_page(comp_name,browser) #open the master window with all info displayed on the same page

                            #page = browser.page_source
                            #crd = get_crd_from_page(page)

                            return crd

                except:
                    continue
        except:
            #href = browser.find_element_by_xpath("//*[@title='Link to BrokerCheck']")
            browser.back() #only need to go back one step
            time.sleep(0.5)
            return "Brokage Firm"

def save_full_page(comp_name,browser):
    links = browser.find_elements_by_class_name("Nav")
    parent_window = browser.current_window_handle
    for link in links:
        mouseover = link.get_attribute("onmouseover")
        if 'Link To View All' in mouseover:
            link.click()
            time.sleep(2)

            handles = browser.window_handles
            handles.remove(parent_window)
            browser.switch_to_window(handles.pop())
            #page = browser.page_source
            print browser.current_url
            file = open("urls.txt","a")
            file.write(comp_name+"|||"+browser.current_url)
            file.write("\n")
            time.sleep(0.5)
            browser.close()

            browser.switch_to_window(parent_window)
            browser.back()
            browser.back()
            browser.back()
            time.sleep(0.5)
    return browser

def get_crd_from_page(page):

    soup = BeautifulSoup(page)
    bs = soup.find_all("b")
    for b in bs:
        if "IARD/CRD Number" in b.get_text():
            font = b.find("font")
            if font != None:
                print font.get_text()
                return font.get_text()
            else:
                crd = b.find("span")
                print crd.get_text()
                return crd.get_text()

def find_data(company,browser,page):
    data = extract_first_page(page)
    browser.back()
    browser.back()
    browser.back()
    return data

if __name__ == "__main__":
    initialize_csv('output_A.csv')
    #make a column after crd to capture state/sec  4,5,8,9,12

    for search_keyword in search_keywords_combinations_a:
        company_names,browser = get_company_names(search_keyword)
        error_companies = []
        for company in company_names:
            try:
                page = find_crd(company[0],browser)
                #company.append(crd)
                #extract_data = find_data(company[0],browser,page)
                #print "extract_data"
                #print extract_data
                #filename = "output/{!s}.csv".format(company[0])

                #initialize_company_csv(filename)
                #write_company_info(extract_data,filename)
                #write(company_names,'output_A.csv')

                company_names.remove(company)
            except: #catch all exceptions and record the companies with errors
                error_companies.append(company)

        browser.close()