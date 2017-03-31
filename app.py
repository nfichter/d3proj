from flask import Flask, render_template
import urllib2, json, csv
from django.utils.safestring import mark_safe

app = Flask(__name__)
key = "AIzaSyCribAPQyNvWFjOt0g66YjJVP_q2REPvoE"

#format City name for querey
def formatCity(name):
    ans = str.split(name)
    return "+".join(ans)


@app.route("/")
def root():
    CSVreports = getReports()
    reports = []
    isWorking = 0 #counter
    for report in CSVreports:
        print isWorking
        isWorking = isWorking + 1
        if isWorking <  50:
            result = getData(report["City"],report["State"],report["Summary"])
            if result != False:
                reports.append(result)
    #print json.dumps(data['results'][0], indent=4, sort_keys=True)
    #print reports
    return render_template("d3test.html", reports=mark_safe(reports))
def getData(city,state,specs):
    city = formatCity(city)
    u = urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address="+city+",+"+state+"&key="+key)
    response = u.read()
    data = json.loads( response )
    if data['status'] == 'OK':
        return {mark_safe("lat"):data['results'][0]['geometry']['location']['lat'],mark_safe("lng"):-1*data['results'][0]['geometry']['location']['lng'],mark_safe("state"):mark_safe(state),mark_safe("city"):mark_safe(city),mark_safe("specs"):mark_safe(specs)}
    return False

def getReports():
    reports = csv.DictReader(open('data/2017.csv')) #need to figure out slider interaction
    return reports

if __name__ == "__main__":
    app.debug = True
    app.run()
