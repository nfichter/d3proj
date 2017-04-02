import urllib2, re, os.path

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
    test = urllib2.urlopen(link)
    u = re.sub(c, '', test.read())
    while u[0:4] != 'Date':
        u = u[1:]
    u = u.strip()
    u = u.split('\r\n')
    ret = []
    fname = 'data/' + dates[m][0:4] + '.csv'
    if os.path.isfile(fname):
        i = 7
    else:
        i = 0
    while i < len(u):
        if u[i] == 'Date / Time' or ('/' in u[i] and ':' in u[i]):
            x = 0
            while x < 7:
                r = u[i+x]
                r = r.replace(',', '","')
                ret.append(r)
                x += 1
        i += 1
    f = open(fname, 'a+')
    i = 0
    while i < len(ret):
        if i % 7 == 0 and (ret[i+1] == '' or ret[i+2] == ''):
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
    while i < 3:
        addReport(i, dates)
        print 'Added ' + dates[i][4:] + '/' + dates[i][0:4]
        i += 1

addAll()

'''
    f = open(fname, 'a+')
    i = 0
    while i < len(ret):
        if i % 7 == 0 and (ret[i+1] == '' or ret[i+2] == ''):
            i += 7
        else:
            if i % 7 != 6:
                f.write(ret[i] + ',')
            else:
                f.write(ret[i] + '\n')
            i += 1
    f.close()
'''
