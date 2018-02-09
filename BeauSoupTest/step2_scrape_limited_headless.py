#!/usr/bin/python
# from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, sys
import time
from bs4 import *
import unicodedata
import re
from bs4 import NavigableString
import csv
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import subprocess

########
#Get all the basic information, and write them to the 'basic.csv'
########
def get_basics(soup, csvf):
    name = soup.title.text
    # print name
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
    name = name.split('-')[0].strip()
    # print name
    alternate_name = soup.find("b", text = re.compile(r'\s*Alternate\s*Names:\s*', re.IGNORECASE))
    if alternate_name:
        alternate_name = alternate_name.parent.text
        alternate_name = unicodedata.normalize('NFKD', alternate_name).encode('ascii', 'ignore')
        alternate_name = alternate_name.split(':')[1].strip()
    else:
        alternate_name = None
    # print alternate_name
    licen = soup.find("img", { "alt" : "Individual registration as a broker, investment advisor, "
                                       "or both"}).parent
    licen = get_header_info(licen)
    # print licen
    disclosure = soup.find("img", { "alt" : "Disclosures including customer complaints, regulatory actions and criminal convictions"
                                       }).parent
    # print disclosure
    disclosure = get_header_info(disclosure)
    # if re.search(r'Less', disclosure):
    #     print disclosure, 'less/n'
    #     disclosure = 0
    # else:
    #     print disclosure, 'not less/n'
    if re.search(r'\d+', disclosure):
        disclosure = int(re.search(r'\d+', disclosure).group())
    else:
        disclosure = 0
    employ = soup.find("img", { "alt" : "Employment and registration history"}).parent
    employ = get_header_info(employ)
    employ = int(re.search(r'\d+',employ ).group())
    exam = soup.find("img", { "alt" : "Qualifications: exams passed and state licenses"}).parent
    exam = get_header_info(exam)
    exams = int(re.search(r'\d+', exam).group())
    if len(re.findall(r'\d+', exam))>1:
        state = int(re.findall(r'\d+', exam)[1])
    else:
        state = 0

    if skip_limit(soup):
        limit = 1
    else:
        limit = 0
    data = [name, alternate_name, licen, disclosure, employ, exams, state, limit]
    print data

    if data:
        with open(csvf, 'a') as cf:
            writer = csv.writer(cf)
            # i_crd+=1
            # print data
            writer.writerow([crd]+ data)

    return data

########
# parse the text for information
########
def get_header_info(header):
    # print header
    header = header.next_element.next_element.next_element.text
    # print header
    header = unicodedata.normalize('NFKD', header).encode('ascii', 'ignore')
    # header = [' '.join(a) for a in header.splitlines()]
    data = ' '.join(header.strip().split())
    # print data
    # data = ' '.join(data)
    # print data
    return data

def print_row(data):
    for row in data:
        print len(row),row

########
#unused function
########
def store_info(data, crd):
    headers = ['crd','name', 'alternate_name', 'license', 'disclosure', 'registraion','exams', 'states']
    table =[]
    # table.append(headers)
    table.append([crd] + data)
    return table

########
#Scrape the disclosure and store in the disclosure.csv
########
def get_disclosure(driver, data, soup, csvf):
    #basic_disclosure = data[4]
    # number_of_disclosure = int(re.search(r'\d+', data[3]).group())
    number_of_disclosure = data[3]

    #IF THERE IS ANY, OPEN THE DISCLOSURE LINK.
    disclosures = []
    if number_of_disclosure > 0:
        CURRENT_Disc = soup.find(text = re.compile('Disclosure Event\(s\)')).parent.parent
        # print number_of_disclosure
        for i in range(0,number_of_disclosure):
            NEXT_Disclosure = CURRENT_Disc.next_sibling.next_sibling
            arrow_id =  NEXT_Disclosure.next_sibling.next_sibling.get('id').strip()
            #print arrow_id, type(arrow_id), '\n'
            if i%2 == 0:
                list = i+1
                elem = driver.find_element_by_xpath("/html[@class='Chrome js responsive']/body/div[@class='content-area "
                                                "finrabrand_container']/div[5]/div[@id='labelCell']/div["
                                                "@id='contentTable']/div[@class='Padding15']/div["
                                                "@class='SummarySectionColor'][2]/div[@class='bcrow  "
                                                "left-border']/div[@class='summarysectionrightpanel']/div["
                                                "@id='dvDiscContent']/table[@id='disclosureSection']/tbody/tr["
                                                "6]/td/table[@id='disclosuretable']/tbody/tr["
                                                "@class='ListItemColor'][%s]/td[@id='evnt']/div[@class='NoPadding']"
                                                "/span[@id='plus']"% list)
            else:
                list = i
                elem = driver.find_element_by_xpath("/html[@class='Chrome js responsive']/body/div["
                                                    "@class='content-area "
                                                "finrabrand_container']/div[5]/div[@id='labelCell']/div["
                                                "@id='contentTable']/div[@class='Padding15']/div["
                                                "@class='SummarySectionColor'][2]/div[@class='bcrow  "
                                                "left-border']/div[@class='summarysectionrightpanel']/div["
                                                "@id='dvDiscContent']/table[@id='disclosureSection']/tbody/tr["
                                                "6]/td/table[@id='disclosuretable']/tbody/tr["
                                                "@class='AlternateListItemColor'][%s]/td[@id='evnt']/div["
                                                "@class='NoPadding']/span[@id='plus']"% list)

            driver.execute_script("$(arguments[0]).click();", elem )
            time.sleep(1)
            html = driver.page_source
            soup = BeautifulSoup(html)
            # print html
            CURRENT_Disc = soup.find(id = arrow_id )
            # event_raw = CURRENT_Disc.previous_sibling.previous_sibling.get_text()
            event = unicodedata.normalize('NFKD', CURRENT_Disc.previous_sibling.previous_sibling.get_text() ).encode(
                'ascii', 'ignore')
            # header = [' '.join(a) for a in header.splitlines()]
            event = ' '.join(event.strip().split())
            # print event, type(event)
            event = re.split(r'([0-3][0-9]/[0-3][0-9]/(?:[0-9][0-9])?[0-9][0-9])', event)
            event = filter(bool, event)
            # print event
            if len(event) < 2:
                event = [None] + event
            else:
                pass
            # print event

            disclosure = []
            #print CURRENT_Disc.findAll('div', {"class" : "disclosureInnerDiv"})
            for div in CURRENT_Disc.findAll('div', {"class" : "disclosureInnerDiv"}):
                # print div#.parent
                row = ''
                for element in div.contents:
                    text = unicodedata.normalize('NFKD', element.text).encode('ascii', 'ignore')
                    row += text + ": "
                disclosure.append(row.rstrip(': '))
                # print disclosure
            disclosures.append([event[0]]+[event[1]]+[disclosure])
        # print i,disclosure
    else:
        disclosures.append(None)
    # print_row(disclosures)
    with open(csvf, 'a') as cf:
        writer = csv.writer(cf)
        for row in disclosures:
            if row:
                writer.writerow([crd]+row)
    return disclosures

########
#scrape the examination and store it in the exam.csv
########
def get_exam(data,soup, csvf):
    # num_exams = int(re.search(r'\d+', data[5]).group())
    # print num_exams
    exams = []
    # if num_exams > 0:
    first = soup.find_all("img", { "alt" : "Qualifications: exams passed and state licenses"})
    if len(first)>1:
        first = first[1].parent.parent
        first = first.find_next_sibling()
        current = first.next_element.next_element.next_element.next_element.next_element.next_element
        if current is not None:
            # print current
            while (current.next_sibling.next_sibling):
                current = current.next_sibling.next_sibling
                # print type(current)
                if not isinstance(current,NavigableString):
                    contents = current.contents
                    exam = []
                    for i in range(len(contents)):
                        if not isinstance(contents[i],NavigableString):
                            # print i, contents[i].get_text()
                            text = unicodedata.normalize('NFKD', contents[i].get_text()).encode('ascii', 'ignore')
                            text = ' '.join(text.strip().split())

                            exam.append(text)
                    # print exam
                    exams.append(exam)
                if  current.next_sibling is None or current is None:
                    break
        results = []
        # print exams
        for i, exam in enumerate(exams):
            if len(exam) > 1:
                # print exam, type(exam)
                for i in range(1,len(exam)):
                    result = []
                    result.append(exam[0])
                    text = re.split(r'([0-3][0-9]/[0-3][0-9]/(?:[0-9][0-9])?[0-9][0-9])', exam[i])
                    text = filter(bool, text)
                    result += text
                    results.append(result)
    else:
        results = []
    # print results
    with open(csvf, 'a') as cf:
        writer = csv.writer(cf)
        for row in results:
            # if row and len(prev_regs) ==1:
            #     writer.writerow([crd]+[row])
            if row:
                writer.writerow([crd]+row)
    return results

########
#get the registration and store it in the reg.csv
########
def get_reg(data,soup, csvf):
    prev_regs = []
    current_regs = []
    current_reg = soup.find(text = re.compile('Current Registration\(s\)'))
    if current_reg:
        current_reg=current_reg.parent.parent

        current_reg = current_reg.next_sibling.next_sibling
        text = unicodedata.normalize('NFKD', current_reg.get_text()).encode('ascii', 'ignore')
        text = ' '.join(text.strip().split())
        current_regs.append(text)
        current_regs = filter(bool, current_regs)
    else:
        current_regs=[]
    # print current_regs

    prev_reg = soup.find(text = re.compile('Previous Registration\(s\)'))
    if prev_reg:
        prev_reg=prev_reg.parent.parent
        prev_reg = prev_reg.next_sibling.next_sibling
        contents = prev_reg.contents
        # print_row(prev_reg)
        for i in range(len(contents)):
            if not isinstance(contents[i],NavigableString):
                text = unicodedata.normalize('NFKD', contents[i].get_text()).encode('ascii', 'ignore')
                text = ' '.join(text.strip().split())
                prev_regs.append(text)

        prev_regs = filter(bool, prev_regs)
    else:
        prev_regs=[]
    # print prev_regs
    with open(csvf, 'a') as cf:
        writer = csv.writer(cf)
        for row in current_regs:
            if row:
                # if row and len(current_regs)==1:
                writer.writerow([crd]+[row] +[1])
                # if row:
                #     writer.writerow([crd]+row)
        for row in prev_regs:
            if row:
                # if row and len(prev_regs) ==1:
                writer.writerow([crd]+[row]+[0])
                # if row:
                #     writer.writerow([crd]+row)
    return current_regs, prev_regs

########
#unused
########
def writeToCSV(matrix, filePath, type):
    thisFile = open(filePath, type)
    writer = csv.writer(thisFile)
    for row in matrix:
        writer.writerow(row)
    thisFile.close()

########
#some crd/individual has limited information. So this gives a check for that. 
########
def skip_limit(soup):
    elem = soup.find(text = re.compile(
        r'\s*BrokerCheck\s*contains\s*very\s*limited\s*information\s*for\s*this\s*broker.', re.IGNORECASE))
    if elem:
        return 1
    return 0

########
#overall function that scrape the 'basic.csv', 'reg.csv', and 'exam.csv'
########
def curl_scrap(crd, basicf, regf, examf):
    cmd = 'curl -s http://brokercheck.finra.org/Individual/Summary/' + crd
    html= subprocess.check_output(cmd, shell = True)
    soup = BeautifulSoup(html)
    data = get_basics(soup, basicf)

    current_regs, prev_regs = get_reg(data,soup, regf)
    exams = get_exam(data, soup, examf)
    return current_regs, prev_regs, exams

if __name__ == '__main__':
    with open('exam.csv','w') as af,open('basic.csv','w') as bf,open('reg.csv','w') as cf,open('disclosure.csv','w') as df:
        writer = csv.writer(af)
        writer.writerow(['CRD', 'Type', 'Exam', 'Date'])
        writer = csv.writer(bf)
        writer.writerow(['CRD','Name','Alternate_name','License(s)','Disclosure(s)', 'Year(s) in Securities',
                         'Exam(s)',
                         'State(s)', 'Limited'])
        writer = csv.writer(cf)
        writer.writerow(['CRD', 'Registration(s)', 'Current/Previous'])
        writer = csv.writer(df)
        writer.writerow(['CRD', 'Date', 'Event Name', 'Information'])
    #with open('failed.txt', 'w') as failf:
    #    failf.write("")
    with open('/Users/bill/PycharmProjects/BeauSoupTest/re_run_crds.csv', 'r') as f:
        reader = csv.reader(f)
        crds = list(reader)
        crds = [i[0] for i in crds]
        crds = [i.zfill(7) for i in crds]

    ########
    # restart control
    ########
    if len(sys.argv)>1:
        # print(sys.argv)
        start = int(sys.argv[1])
    else:
        start = 0
    end = int(len(crds))
    # crds =  crds[start:end]

    # display = Display(visible=0, size=(800,600))
    # display.start()

    #starting a driver
    # /Users/bill/PycharmProjects/BeauSoupTest/step2_scrape_limited_headless.py
    chromedriver = '/Users/bill/PycharmProjects/BeauSoupTest//chromedriver'
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    url = "http://brokercheck.finra.org"
    driver.get(url)

    for i_crd, crd in enumerate(crds[start:]):
        #######
        #Try-Except loop to restart the code if there is a NoSuchElementException or WebDriverException
        #######
        try:
            print("Processing " + str(crds.index(crd)) + ', ' + str(crd) + " from " + str(start)+ " to " + str(end) )
            # curl_scrap(crd,'basic.csv', 'reg.csv', 'exam.csv')

            # Getting past the Term&Condition Agreement
            elem = driver.find_elements_by_xpath("//div[div[input[@type = 'submit' and @id = "
                                                 "'ctl00_phContent_TermsAndCondUC_BtnAccept']]]//input")
            if len(elem) > 1:
                driver.execute_script("$(arguments[0]).click();", elem[0] )
                time.sleep(1)
            else:
                pass

            #########
            #Crawl to the new page. 
            ########
            if i_crd == len(crds):
                break
            else:
                key = crd
            elem = driver.find_element_by_id('GenericSearch_IndividualSearchText')
            elem.clear()
            elem.send_keys(key)
            time.sleep(0.5)
            elem.submit()

            ####
            # Click open all the link and scrape the disclosure information. Store it in 'disclosure.csv'
            ####
            html = driver.page_source
            soup = BeautifulSoup(html)
            data = get_basics(soup, 'basic.csv')
            exam = get_exam(data,soup, 'exam.csv')
            registration = get_reg(data, soup, 'registration.csv')
            disclosures = get_disclosure(driver, data, soup, 'disclosure.csv')

        except AttributeError, e:
            # driver.close()
            with open('failed.txt', 'a') as tf:
                tf.write(str(crd) + ': ' + str(e) + "\n")
        except NoSuchElementException, e:
            driver.close()
            # display.popen.kill()
            print "Start New Driver" + str(e)
            os.execv('/local/bill_test/finra/Limited/step2_scrape_limited_headless.py', (str(crds.index(crd)), str(crds.index(crd))))
        except WebDriverException, e:
            driver.close()
            # display.popen.kill()
            print "Start New Driver" + str(e)
            os.execv('/local/bill_test/finra/Limited/step2_scrape_limited_headless.py', (str(crds.index(crd)), str(crds.index(crd))))
        # except Exception, e:
        #     with open('failed_crd.txt', 'a') as tf:
        #         tf.write(str(crd) + ': ' + str(e) + "\n")
    driver.close()
    # display.popen.kill()
