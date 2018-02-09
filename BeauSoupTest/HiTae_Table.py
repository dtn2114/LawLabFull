from bs4 import BeautifulSoup
from collections import defaultdict
import re

class Table(object):
    # Create based on file type information:
    def factory(content, file_type):
        if file_type == "HTML":
            return HtmlTable(content)
        if file_type == "TEXT":
            return TextTable(content)
        assert 0, "Bad table creation: " + file_type
    factory = staticmethod(factory)


def remove_empty_cols_rows(data):
    data = [list(row) for row in data if any(row)]
    zip(*data)
    data = [list(row) for row in data if any(row)]
    zip(*data)
    return data


def balance_rows(data, num_col):
    for i, row in enumerate(data):
        diff = num_col - len(row)
        if diff:
            row = row + [''] * diff
        data[i] = row
    return data


class HtmlTable(Table):
    def __init__(self, content):
        self.content = content
        self.soup = BeautifulSoup(content)
        self.data = self.get_data()
        self.classify_string = ''

    def get_data(self):
        table = self.soup.find("table")
        # balance table using colspan, rowspan
        result = defaultdict(lambda: defaultdict(unicode))
        try:
            for row_i, row in enumerate(table.find_all('tr')):
                for col_i, col in enumerate(row.find_all('td')):
                    colspan = int(col.get('colspan', 1))
                    rowspan = int(col.get('rowspan', 1))
                    col_data = " ".join(col.strings).encode('ascii', 'replace').replace('?', ' ').replace('\n', ' ')
                    while row_i in result and col_i in result[row_i]:
                        col_i += 1
                    for i in range(row_i, row_i + rowspan):
                        for j in range(col_i, col_i + colspan):
                            result[i][j] = col_data
            data = []
            num_col = 0
            for i, row in sorted(result.items()):
                cols = []
                for j, col in sorted(row.items()):
                    cols.append(col.strip())
                if len(cols) > num_col:
                    num_col = len(cols)
                data.append(cols)
            data = balance_rows(data, num_col)
            data = remove_empty_cols_rows(data)
            return data
        except AttributeError:
            return []
        except ValueError:
            return []

    def get_lines_with(self, keywords):
        lines = []
        # combine two rows if they are for the same exhibit number
        for row in self.data:
            if row[0]:  # there is a exhibit number
                lines.append(' '.join(row))
            else:
                if lines:
                    lines.append(lines.pop() + ' ' + ' '.join(row))
                else:
                    lines.append(' '.join(row))
        rows = lines
        lines = []
        # split one line into two if there is a separator, ;
        for row in rows:
            if ";" in row:
                entries = row.split(";")
                for entry in entries:
                    lines.append(entry)
            else:
                lines.append(row)
        rows = lines
        lines = []
        for row in rows:
            if any(keyword.lower() in row.lower() for keyword in keywords):
                lines.append(row.strip())
        return lines

    def get_num_rows(self):
        return len(self.data)

    def get_num_cols(self):
        return len(self.data[0])

    def find_header_rows(self, keywords):
        headers = []
        max_num_header_rows = 4
        for row in self.data[:max_num_header_rows]:
            if any(keyword.lower() in " ". join(row).lower() for keyword in keywords):
                headers.append(row)
        return headers

    def has_keywords(self, keywords):
        for row in self.data:
            if any(keyword.lower() in " ".join(row).lower() for keyword in keywords):
                return True
        return False

    def has_all_keywords_headers(self, keywords):
        str_table = ""
        for row in self.data[:2]:
            str_table += " ".join(row).lower()
        if all(keyword.lower() in str_table for keyword in keywords):
            return True
        else:
            return False

    def get_type(self):
        return "HTML"


class TextTable(Table):
    def __init__(self, content):
        self.content = content
        self.lines = content.splitlines()
        self.data_intervals = []
        self.heading_intervals = []
        self.heading_block = []
        self.headings = []
        self.classify_string = ''
        self.rows = []
        self.data_start = 0
        self.caption_start = 0
        self.data = []
        self.to_avoid = ['___', '---']

    def get_num_rows(self):
        return len(self.data)

    def get_num_cols(self):
        return len(self.data[0])

    def get_type(self):
        return "TEXT"

    def process (self):
        self.find_data_intervals()
        self.find_headings()
        self.find_rows()
        self.data = [self.headings] + self.rows

    def find_data_intervals (self):
        # find <C> tags
        for line in self.lines:
            if '<caption>' in line.lower():
                self.caption_start = self.lines.index(line)
            boundaries = [m.start() for m in re.finditer('<c>', line.lower())]
            if (boundaries):
                self.data_start = self.lines.index(line)
                # append the length of the longest line in table
                boundaries.append(len(max(self.lines, key=len)))
                break

        previous = 0
        for b in boundaries:
            self.data_intervals.append([previous, b])
            previous = b

    def find_heading_intervals(self):
        # last line of the list is the closest to the bottom
        first_line = self.heading_block[-1]

        # old RE: (\S+\s?\S+)+
        #create a list of lists containing the start and end indices for each match
        boundaries = [[m.start(), m.end()] for m in re.finditer('(?:\S+(?:\s\S+)*)', first_line)]

        # all lines but the last
        minus_last = self.heading_block[:-1]

        for line in minus_last:
            # create a list of the new indices
            temp_boundaries = [(m.start(), m.end()) for m in re.finditer('(?:\S+(?:\s\S+)*)', line)]
            for temp in temp_boundaries:
                new_start = temp[0]
                for i in range(0, len(boundaries)-1):
                    bound1 = boundaries[i][1]
                    bound2 = boundaries[i+1][0]

                    if new_start > bound1 and new_start < bound2:
                        boundaries[i+1][0] = new_start
                else:
                    continue

        # take the starting value of each division (minus the first)
        boundary_list = [b[0] for b in boundaries[1:]]
        # append the longest line
        boundary_list.append(len(max(self.heading_block, key=len)))

        previous = 0
        for b in boundary_list:
            self.heading_intervals.append([previous, b])
            previous = b

    def find_headings (self):
        '''
        figure out how to get self.heading_block
        '''
        rows =  self.lines[self.caption_start+1:self.data_start]

        # build string for table classification
        classify_block = [element.strip() for element in rows]
        classify_block = " ".join(classify_block).lower().strip()
        classify_block = classify_block.replace('--', '').replace('__', '')
        self.classify_string = classify_block

        first_line_index = len(rows)-1
        last_line_index = 0
        first_line = None
        first_found = False
        for row in reversed(rows):
            #if row:
            # non-divider and non-empty string encountered, so first line encountered
            if not (first_found) and not ((row.isspace()) or (any(word in row for word in self.to_avoid))):
                first_found = True
                first_line_index = rows.index(row)
            # whitespace or divider encountered, so headings are completed
            elif (first_found) and (row.isspace() or any(word in row for word in self.to_avoid)):
                last_line_index = rows.index(row) + 1
                break
            else:
                pass

        self.heading_block = rows[last_line_index:first_line_index+1]
        self.find_heading_intervals()
        self.break_by_heading_interval(self.heading_block)

    def find_rows (self):
        self.rows = [self.break_by_data_interval(self.lines[i])
                   for i in range(self.data_start + 1, len(self.lines) - 1)
                   if (self.lines[i]) and not any(word in self.lines[i] for word in self.to_avoid)]

    def break_by_data_interval (self, line):
        row = []
        for interval in self.data_intervals:
            row.append(line[interval[0]:interval[1]].strip())
        return row

    def break_by_heading_interval (self, to_break):
        for interval in self.heading_intervals:
            heading_composition = []
            for line in to_break:
                heading_composition.append(line[interval[0]:interval[1]].strip())
            heading = ' '.join(heading_composition).strip()
            self.headings.append(heading)

if __name__ == '__main__':
    #path = '/Users/bill/PycharmProjects/BeauSoupTest/comp_table/'
    with open('/Users/bill/PycharmProjects/BeauSoupTest/companies/MSFT/0001193125-03-051346_789019_1.txt',
              'r') as f:
        table_doc = f.read()
        tables = re.findall(r'<table.+?</table>', table_doc, re.DOTALL | re.IGNORECASE)
        t_count = 0
        for t in tables:
            pt = Table.factory(t, 'HTML').data
            print pt