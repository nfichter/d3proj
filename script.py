import urllib2, re, os.path, app

c = re.compile('<.*?>')

def getDates():
    url = urllib2.urlopen('http://www.nuforc.org/webreports/ndxevent.html')
    u = url.read()
    u = re.sub(c, '', u)
    while u[len(u)-4:len(u)] != '1905':
        u = u[:len(u)-1]
    
    u = u.replace('\r', '')
    u = u.replace('\n\n\n\n\n', '\n')
    u = u.split('\n')

    dates = []
    for month in u:
        if len(month) == 7 and month[2] == '/':
            d = month[3:] + month[:2]
            dates.append(d)

    return dates

def addReport(m, dates):
    link = 'http://www.nuforc.org/webreports/ndxe' + dates[m] + '.html'
    u = urllib2.urlopen(link).read()
    u = re.sub(c, '', u)
    u = u[u.find('Date'):]
    u = u.strip()
    u = u.split('\r\n')
    ret = []
    fname = 'data/' + dates[m][0:4] + '.csv'
    if os.path.isfile(fname):
        i = 7
    else:
        i = 0
    while i < len(u):
        if u[i] == 'Date / Time' or ('/' in u[i] and u[i][len(u[i])-3] == ':'):
            x = 0
            while x < 7:
                r = '"' + u[i+x] + '"'
                if r == '""':
                    r = '"N/A"'
                ret.append(r)
                x += 1
        i += 1
    f = open(fname, 'a+')
    i = 0
    while i < len(ret):
        if i % 7 == 0 and (ret[i+1] == '"N/A"' or ret[i+2] == '"N/A"'):
            i += 7
        else:
            if i % 7 != 6:
                f.write(ret[i] + ',')
            else:
                f.write(ret[i] + '\n')
            i += 1
    f.close()
        
def addAll():
    dates = getDates()
    i = 0
    while i < len(dates):
        addReport(i, dates)
        print 'Added ' + dates[i][4:] + '/' + dates[i][0:4]
        i += 1

#addAll()

def reportCount():
    dates = getDates()
    count = 0
    i = 0
    year = ''
    while i < len(dates):
        if dates[i][0:4] != year:
            year = dates[i][0:4]
            fname = 'data/' + year + '.csv'
            if os.path.isfile(fname):
                f = open(fname)
                lines = f.readlines()
                f.close()
                numReports = len(lines)-1
                count += numReports
                if numReports == 0:
                    print 'REMOVING ' + year
                    os.remove(fname)
                print year + ': ' + str(numReports) + ' reports'
            else:
                print year + ' HAS BEEN REMOVED'
        i += 1
    print 'Total: ' + str(count) + ' reports'

def formatAll():
    dates = getDates()
    year = ''
    i = len(dates)-1
    while i >= 0:
        year = dates[i][0:4]
        original = 'data/' + year + '.csv'
        if os.path.isfile(original):
            fname = 'data/formatted' + year + '.csv'
            if os.path.isfile(fname):
                pass
            else:
                print 'Formatting ' + year
                app.CSVtoFormattedCSV(year)
        i -= 1

formatAll()
        
#reportCount()
