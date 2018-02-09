__author__ = 'yutingchen'

from bs4 import BeautifulSoup
from global_setting_parsing import *
import csv
import time

#come back to this part later
def extract_ScheduleDRP_part1(file,date,comp_name):
    data = []
    soup = BeautifulSoup(open(file))
    no_criminal = soup.find('span',{'id':DRP_no_Criminal})
    if no_criminal != None:
        row = []
        row.append(date)
        row.append(comp_name)
        row.append('No criminal info')
        data.append(row)
    else:
        criminal = soup.find('span',{'id':DRP_Criminal})
        tables = criminal.parent.parent.parent.parent.find_all('table',{'id':'mainTable'})
        for table in tables:
            row = []
            row.append(date)
            row.append(comp_name)
            imgs = table.find_all('img')
            spans = table.find_all('span')
            if "not" not in imgs[0]['alt']:
                row.append("initial")
            else:
                row.append('amended')

            for i in range(2,6):
                if "not" not in imgs[i]['alt']:
                    row.append(1)
                else:
                    row.append(0)

            if "not" not in imgs[6]['alt']:
                row.append("You")
            elif "not" not in imgs[7]['alt']:
                row.append("You and one or more of your advisory affiliates")
            elif "not" not in imgs[8]['alt']:
                row.append("One or more of your advisory affiliates")

            if "not" not in imgs[9]['alt']:
                row.append("Firm")
            elif "not" not in imgs[10]['alt']:
                row.append("Individual")
            else:
                row.append("N/A")

            if "not" not in imgs[11]['alt']:
                row.append("Yes")
            elif "not" not in imgs[12]['alt']:
                row.append("No")
            else:
                row.append("N/A")

            #Name of advisory affiliate
            row.append(spans[2].get_text().encode('ascii', 'ignore'))

            for i in range(13,17):
                if "not" not in imgs[i]['alt']:
                    row.append(1)
                else:
                    row.append(0)

            for j in range(4,8):
                row.append(spans[j].get_text().encode('ascii', 'ignore'))

            if "not" not in imgs[18]['alt']:
                row.append("Exact")
            elif "not" not in imgs[19]['alt']:
                row.append("Explanation")
            else:
                row.append("N/A")

            for k in range(8,9):
                row.append(spans[k].get_text().encode('ascii', 'ignore'))

            if "not" not in imgs[20]['alt']:
                row.append("Yes")
            elif "not" not in imgs[21]['alt']:
                row.append("No")
            else:
                row.append("N/A")
            if "not" not in imgs[22]['alt']:
                row.append("Pending")
            elif "not" not in imgs[23]['alt']:
                row.append("On Appeal")
            elif "not" not in imgs[24]['alt']:
                row.append("Final")
            else:
                row.append("N/A")

            row.append(spans[9].get_text().encode('ascii', 'ignore'))
            if "not" not in imgs[25]['alt']:
                row.append("Exact")
            elif "not" not in imgs[26]['alt']:
                row.append("Explanation")
            else:
                row.append("N/A")
            for l in range(10,13):
                row.append(spans[l].get_text().encode('ascii', 'ignore'))

            data.append(row)
    print data
    return data

def extract_ScheduleDRP_part2(file,date,comp_name):
    data = []
    soup = BeautifulSoup(open(file))
    no_regulatory = soup.find('span',{'id':DRP_no_regulatory})
    if no_regulatory != None:
        row = []
        row.append(date)
        row.append(comp_name)
        row.append('No regulatory info')
        data.append(row)
    else:
        regulatory = soup.find('span',{'id':DRP_regulatory})
        tables = regulatory.parent.parent.parent.parent.find_all('table',{'id':'mainTable'})

        for table in tables:
            row = []
            row.append(date)
            row.append(comp_name)
            spans = table.find_all("span")
            imgs = table.find_all('img')
            if len(spans)>23:
                if "not" not in imgs[0]['alt']:
                    row.append("initial")
                else:
                    row.append('amended')
                for i in range(0,16):
                    j = i+2
                    if "not" not in imgs[j]['alt']:
                        row.append(1)
                    else:
                        row.append(0)
                if "not" not in imgs[18]['alt']:
                    row.append("You")
                elif "not" not in imgs[19]['alt']:
                    row.append("You and one or more of your advisory affiliates")
                elif "not" not in imgs[20]['alt']:
                    row.append("One or more of your advisory affiliates")

                for k in [21,22,23]:
                    if "not" not in imgs[k]['alt']:
                        row.append(1)
                    else:
                        row.append(0)
                if "not" not in imgs[24]['alt']:
                    row.append("Yes")
                elif "not" not in imgs[25]['alt']:
                    row.append("No")
                else:
                    row.append('N/A')

                if "not" not in imgs[26]['alt']:
                    row.append("SEC")
                elif "not" not in imgs[27]['alt']:
                    row.append("Other Federal")
                elif "not" not in imgs[28]['alt']:
                    row.append("State")
                elif "not" not in imgs[29]['alt']:
                    row.append("SRO")
                elif "not" not in imgs[30]['alt']:
                    row.append("Foreign")
                else:
                    row.append('N/A')


                for i in [3,5,6,7,8,9,10,12,13,14]:
                    row.append(spans[i].get_text().encode('ascii', 'ignore'))

                if "not" not in imgs[33]['alt']:
                    row.append("Pending")
                elif "not" not in imgs[34]['alt']:
                    row.append("On Appeal")
                elif "not" not in imgs[35]['alt']:
                    row.append("Final")
                else:
                    row.append('N/A')

                for i in [15,17,18,19]:
                    row.append(spans[i].get_text().encode('ascii', 'ignore'))

                for j in range(36,43):
                    if "not" not in imgs[j]['alt']:
                        row.append(1)
                    else:
                        row.append(0)

                for k in range(20,24):
                    row.append(spans[k].get_text().encode('ascii', 'ignore'))
                data.append(row)
        print data
    return data


def write_DRP_xlsx(filename,file):
    """create csv file for schedule A's """
    try:
        wb = xlwt.Workbook()
        ws = wb.add_sheet('DRP_part2')
        for i in range(0,len(DRP_part2_col_header)):
            ws.write(0,i,DRP_part2_col_header[i])

        soup = BeautifulSoup(open(file))
        data = extract_ScheduleDRP_part2(soup)
        for i in range(0,len(data)):
            for j in range(0,len(data[i])):
                ws.write(i+1,j,data[i][j])

        wb.save(filename)
    except:
        raise

def initialize_DRP_csv_part1(filename):
    """create csv file for schedule A's """
    try:
        outfile = open(filename, "wb")
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_ALL)
        for row in DRP_part1_col_header:
            writer.writerow(row)
        outfile.close()
    except:
        raise

def initialize_DRP_csv_part2(filename):
    """create csv file for schedule A's """
    try:
        outfile = open(filename, "wb")
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_ALL)
        for row in DRP_part2_col_header:
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