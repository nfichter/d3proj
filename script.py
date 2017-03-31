import urllib2, re

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

dates = getDates()


link = 'http://www.nuforc.org/webreports/ndxe' + dates[len(dates)-1] + '.html'
test = urllib2.urlopen(link)
u = re.sub(c, '', test.read())
while u[0:4] != 'Date':
    u = u[1:]
while u[len(u)-1:len(u)] == '\n':
    u = u[:len(u)-2]
u = u.replace('\r', '')
u = u.split('\n')

i = 0
while i < len(u):
    if u[i] == '\n':
        u.remove(u[i])
    else:
        i += 1
print u
print len(u)
'''
u = u.replace('\n\n\n\n\n', '')
u = u.replace('\n\n', '\nN/A\n')
#print u
u = u.split('\n')
#print u
#print len(u)
'''
