import urllib2, re

c = re.compile('<.*?>')


url = urllib2.urlopen('http://www.nuforc.org/webreports/ndxevent.html')
u = url.read()
u = re.sub(c, '', u)
while u[len(u)-4:len(u)] != '1905':
    u = u[:len(u)-1]

u = u.replace('\r', '')
u = u.replace('\n\n\n\n\n', '\n')
u = u.split('\n')

for month in u:
    print month
    if len(month) != 7:
        u.remove(month)

print u
'''
test = urllib2.urlopen('http://www.nuforc.org/webreports/ndxe201512.html')
u = re.sub(c, '', test.read())
while u[0:4] != 'Date':
    u = u[1:]
while u[len(u)-1:len(u)] == '\n':
    u = u[:len(u)-2]
u = u.replace('\r', '')
print u
u = u.replace('\n\n\n\n\n', '\n')
u = u.split('\n')
'''
