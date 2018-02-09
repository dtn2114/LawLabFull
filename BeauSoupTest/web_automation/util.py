__author__ = 'yutingchen'

import re
import time
import os

DEFAULT_CSV = 'output.csv'

"""
define input validation functions
"""
def is_valid_menu(str):
    """ Return true if str is 1-6, false otherwise. """
    if str.isdigit() and str.__len__() == 1 and \
            int(str) >= 1 and int(str) <= 3:
        return True
    elif str.isdigit() and int(str) == 0:
        return True
    else:
        print("Error: '" + str + "' not valid")
        return False

def is_valid_submenu(str):
    """ Return true if str is 1-6, false otherwise. """
    if str.isdigit() and str.__len__() == 1 and \
            int(str) >= 0 and int(str) <= 4:
        return True
    elif str.isdigit() and int(str) == 0:
        return True
    else:
        print("Error: '" + str + "' not valid")
        return False



def is_yesno(str):
    """ Return true if str is empty or it matches one of 'y', 'yes', 'n', and 'no' while ignoring case, false otherwise. """
    if str.__len__() == 0 or \
            (str.lower() == 'y' or str.lower() == 'n' or str.lower() == 'yes' or str.lower() == 'no'):
        return True
    elif str.isdigit() and int(str) == 0:
        return True
    else:
        return False

def get_yes_no(str):
    yes_no = raw_input(">> " + str + " (y/n) [default: yes]: ")
    while (not is_yesno(yes_no)):
        yes_no = raw_input(">> " + str + " (y/n) [default: yes]: ")
    if yes_no.lower() in ('n', 'no'):
        yes_no = "No"
    elif yes_no.lower() == '0':
        yes_no = "0"
    else:
        yes_no = "Yes"
    return yes_no

def main_menu():
    """
    read menu selection and return the number
    """
    selection = raw_input(">> Enter a number: ")
    while(not is_valid_menu(selection)):
        selection = raw_input(">> Enter a number: ")
    return selection

def sub_menu():
    "read sub menu selection and return the number"
    selection = raw_input(">> Enter a number: ")
    while(not is_valid_submenu(selection)):
        selection = raw_input(">> Enter a number: ")
    return selection

def is_valid_filename(str):
    """ Return true if str ends with '.csv', false otherwise. """
    str = str.replace(':','').lower()
    if str.endswith('.csv') or str.endswith(".xlsx") or str.endswith(".xls"):
        return True
    else:
        print("Error: '" + str + "' not valid")
        return False

def is_valid_crd_range(str):
    "Return the range of crd numbers, return false if range is not valid"
    str = str.replace(':','').lower()
    if "[" not in str or "]" not in str or "," not in str:
        print("Error: '" + str + "' not valid")
        return False
    else:
        #find two numbers
        numbers = re.findall(r"[0-9]+",str)

        if len(numbers)==2:
            return numbers
        else:
            print("Error: '" + str + "' not valid")
            return False

def is_valid_crds(str):
    "return the list of crds if valid, false if the input is not valid"
    is_valid = True
    list_of_crds=[]
    if "," in str:
        numbers = str.split(",")
        for number in numbers:
            print number
            if number.isdigit():
                list_of_crds.append(number)
            else:
                print ("Error: '" + str + "' not valid")
                is_valid = False
                break
    else:
        if str.isdigit():
            list_of_crds.append(str)
    if is_valid:
        return list_of_crds
    else:
        return is_valid

def get_filename(prefix='',default=''):
    """
    read csv filename
    """
    if not default:
        filename = raw_input(">> Enter " + prefix + "filename: [default: " + DEFAULT_CSV + "] ")
    else:
        filename = raw_input(">> Enter " + prefix + "filename: [default: " + default + "] ")
    while(not is_valid_filename(filename)):
        if not default:
            filename = raw_input(">> Enter " + prefix + "filename: [default: " + DEFAULT_CSV + "] ")
        else:
            filename = raw_input(">> Enter " + prefix + "filename: [default: " + default + "] ")
    if not filename:
        if not default:
            return DEFAULT_CSV
        else:
            return default
    else:
        return filename

#return the last modified directory
def getLastModifiedDirectory(path):
    try:
        #Check last updated folder
        file_directory = os.listdir(os.path.abspath(os.getcwd()+"/"+path))
        format = '%Y-%m-%d %H:%M:%S'
        most_recent_time = time.strptime('2000-01-01 00:00:00', format) #hardcode an old time
        for directory in file_directory:
            directory_time = time.strptime(directory, format)

            if directory_time > most_recent_time:
                most_recent_time = directory_time
        most_recent_time = str(time.strftime(format,most_recent_time))
        return most_recent_time
    except:
        print "Cannot get last modified time. Please check if directory exists"
        return None