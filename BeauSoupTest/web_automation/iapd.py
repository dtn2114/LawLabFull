__author__ = 'hs2212'

import requests
import sys
import re
import os
import filecmp
from bs4 import BeautifulSoup


class Iapd:
    def __init__(self, crd):
        """
        initialize Iapd object

        :param crd: CRD number
        :param path: directory path to store html files
        """
        self.crd = crd



    def download_combined(self, path="." , verbose=False):
        """
        download IAPD complete adv form in html format

        :param verbose: output URL if verbose
        :return: None
        """
        url = 'http://www.adviserinfo.sec.gov/IAPD/crd_iapd_AdvVersionSelector.aspx?ORG_PK=' + str(self.crd)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                url_front = response.url
                if url_front == 'http://www.adviserinfo.sec.gov/IAPD/Content/Search/iapd_Search.aspx':
                    print "Error: invalid crd (" + str(self.crd) + ")"
                    return
                else:
                    url_all = url_front.replace('IdentifyingInfoSection', 'AllPages')
                    links = self.get_link_text()
                    for (type, rgltr) in links:
                        url_final = url_all + "&RGLTR_PK=" + rgltr
                        if verbose:
                            print "URL of combined page: " + url_final
                        response_all = requests.get(url_final)
                        if response_all.status_code == 200:
                            page = response_all.text.encode('ascii', 'replace')

                            try:
                                fout = open(path + "/" + str(self.crd) + "_" + type.replace(' ', '_') + ".html", "w")
                                #print os.stat(fout)
                                fout.write(page)
                                fout.close()
                                print "Success: downloaded to " + path + "/" + str(self.crd) + "_" \
                                      + type.replace(' ', '_') + ".html"
                            except IOError:
                                print("Error: failed to write to " + path + "/" + str(self.crd) + "_"
                                      + type.replace(' ', '_') + ".html")
                        else:
                            print ("Error: failed to read from " + url_final)
            else:
                print ("Error: failed to read from " + url)
        except requests.ConnectionError:
            print("Error: failed to read from " + url + ": connection error")
        except requests.HTTPError:
            print("Error: failed to read from " + url + ": invalid response")
        except requests.Timeout:
            print("Error: failed to read from " + url + ": timed out")
        except requests.TooManyRedirects:
            print("Error: failed to read from " + url + ": too many redirects")

    def get_combined(self):
        """
        return IAPD complete adv form in html format

        :return: None if not found, otherwise list of pages in html
        """
        url = 'http://www.adviserinfo.sec.gov/IAPD/crd_iapd_AdvVersionSelector.aspx?ORG_PK=' + str(self.crd)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                url_front = response.url
                if url_front == 'http://www.adviserinfo.sec.gov/IAPD/Content/Search/iapd_Search.aspx':
                    print "Error: invalid crd (" + str(self.crd) + ")"
                    return None
                else:
                    pages = []
                    url_all = url_front.replace('IdentifyingInfoSection', 'AllPages')
                    links = self.get_link_text()
                    for (type, rgltr) in links:
                        url_final = url_all + "&RGLTR_PK=" + rgltr
                        if verbose:
                            print "URL of combined page: " + url_final
                        response_all = requests.get(url_final)
                        if response_all.status_code == 200:
                            page = response_all.text.encode('ascii', 'replace')
                            pages.append(page)
                        else:
                            print ("Error: failed to read from " + url_final)
                    return pages
            else:
                print ("Error: failed to read from " + url)
                return None
        except requests.ConnectionError:
            print("Error: failed to read from " + url + ": connection error")
            return None
        except requests.HTTPError:
            print("Error: failed to read from " + url + ": invalid response")
            return None
        except requests.Timeout:
            print("Error: failed to read from " + url + ": timed out")
            return None
        except requests.TooManyRedirects:
            print("Error: failed to read from " + url + ": too many redirects")
            return None

    def get_link_text(self):
        """
        find which types of information are available. possible values for types are name of state, SEC, or ADV.
        Also, find corresponding RGLTR_PK number and return them as a list of tuple(s).

        :return: list of tuples (link name, rgltr number)
        """
        url = 'http://www.adviserinfo.sec.gov/IAPD/Content/Search/iapd_landing.aspx?SearchGroup=Firm&FirmKey=' \
              + str(self.crd)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                url_front = response.url
                if url_front == 'http://www.adviserinfo.sec.gov/IAPD/Content/Search/iapd_Search.aspx':
                    return None
                page = response.text.encode('ascii', 'replace')
                soup = BeautifulSoup(page)
                links = soup.find_all("a")
                values = []
                for link in links:
                    href = str(link.get('href'))
                    if href.find('ORG_PK') != -1:
                        text = link.get_text()
                        if text.find('ADV') != -1:
                            text = u'ADV'
                        l_rgltr = re.findall(r'RGLTR_PK=(\d+)', href)
                        if l_rgltr:
                            rgltr = l_rgltr.pop()
                        else:
                            rgltr = ''
                        values.append((text, rgltr))
                return values
            else:
                print ("Error: failed to read from " + url)
                return None
        except requests.ConnectionError:
            print("Error: failed to read from " + url + ": connection error")
            return None
        except requests.HTTPError:
            print("Error: failed to read from " + url + ": invalid response")
            return None
        except requests.Timeout:
            print("Error: failed to read from " + url + ": timed out")
            return None
        except requests.TooManyRedirects:
            print("Error: failed to read from " + url + ": too many redirects")
            return None

if __name__ == "__main__":
    """ written for command line execution
    """
    verbose = False
    if len(sys.argv) < 2:
        print 'usage: iapd.py [-v] path [lower_bound upper_bound]'
        exit(1)
    elif len(sys.argv) == 2 and sys.argv[1] == "-v":
        print 'usage: iapd.py [-v] path [lower_bound upper_bound]'
        exit(1)
    elif len(sys.argv) == 3 and sys.argv[1] != "-v":
        print 'usage: iapd.py [-v] path [lower_bound upper_bound]'
        exit(1)
    elif len(sys.argv) == 4 and (sys.argv[1] == "-v" or not sys.argv[2].isdigit() or not sys.argv[3].isdigit()):
        print 'usage: iapd.py [-v] path [lower_bound upper_bound]'
        exit(1)
    elif len(sys.argv) == 5 and (sys.argv[1] != "-v" or not sys.argv[3].isdigit() or not sys.argv[4].isdigit()):
        print 'usage: iapd.py [-v] path [lower_bound upper_bound]'
        exit(1)
    elif len(sys.argv) == 5:
        verbose = True
        path = sys.argv[2]
        lower = sys.argv[3]
        upper = sys.argv[4]
    elif len(sys.argv) == 4:
        path = sys.argv[1]
        lower = sys.argv[2]
        upper = sys.argv[3]
    elif len(sys.argv) == 3:
        verbose = True
        path = sys.argv[2]
        lower = 1
        upper = 200000
    else:
        path = sys.argv[1]
        lower = 1
        upper = 200000

    for crd in range(int(lower), int(upper)+1):
        iapd = Iapd(crd)
        iapd.download_combined(path, verbose)
        #print iapd.get_combined()
        if iapd.get_link_text() != None:
            print str(crd) + ":" + str(iapd.get_link_text())

