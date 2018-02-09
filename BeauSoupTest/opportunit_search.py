#!/usr/bin/python
import subprocess, MySQLdb, time


if __name__ == '__main__':
    db = MySQLdb.connect("localhost", "root", "Edgar20!4", "edgar")
    cursor = db.cursor()
    sql_time = time.time()
    query = "select concat('http://www.sec.gov/Archives/',filename) from edgar limit 250000"
    print "create a list of filenames"
    cursor.execute(query)
    filenames = cursor.fetchall() 
    filenames = [i[0] for i in filenames]
    print("--- sql-time: %s seconds ---" % (time.time() - sql_time))
    summ = 0
    # print filenames
    path = 'http://www.sec.gov/Archives/'
    # filenames = 
    loop_time = time.time()
    for filename in filenames:
        # print "processing " + filename + "..."
        # filename = str(filename[0])
        cmd = 'curl -s ' + filename + "| egrep -c -i '(waive|renounce|disclaim).*(corporate|commercial|business).{0,100}(opportunit)'"
        try:
            i = subprocess.check_output(cmd, shell=True)
            # print 'found'
            summ+=1
            print summ, filename
        except:
            continue
    print("--- loop time: %s seconds ---" % (time.time() - loop_time))
    print summ
