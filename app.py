from flask import Flask, render_template, request
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
    CSVreports = csv.DictReader(open('data/formatted2017.csv'))
    reports = []
    isWorking = 0 #counter
    for report in CSVreports:
        tempReport = {}
        for key in report:
            tempReport[mark_safe(key)] = mark_safe(report[key])
        reports.append(tempReport)
        isWorking = isWorking + 1
    #print json.dumps(data['results'][0], indent=4, sort_keys=True)
    #print reports
    return render_template("index.html", reports=mark_safe(reports))

#ajax to get specific month data
@app.route("/redrawMonth")
def refineData():
    #print fullReport
    year = request.args.get("year")
    month = request.args.get("month")
    day = request.args.get("day")
    CSVreports = csv.DictReader(open('data/formatted'+year+'.csv'))
    result = []
    for report in CSVreports:
        tempReport = {}
        for key in report:
            tempReport[mark_safe(key)] = mark_safe(report[key])
        if day != "":
            reportDay = report["date"].split("/")[1]
            if reportDay == str(day):
                if month != "":
                    reportMonth = report["date"].split("/")[0]
                    if reportMonth == str(month):
                        result.append(tempReport)
        elif month != "":
            reportMonth = report["date"].split("/")[0]
            if reportMonth == str(month):
                result.append(tempReport)
    return json.dumps(result)


def getData(city,state,specs,date,shape,duration):
    city = formatCity(city)
    u = urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address="+city+",+"+state+"&key="+key)
    response = u.read()
    data = json.loads( response )
    if data['status'] == 'OK':
        return {mark_safe("lat"):data['results'][0]['geometry']['location']['lat'],mark_safe("lng"):-1*data['results'][0]['geometry']['location']['lng'],mark_safe("state"):mark_safe(state),mark_safe("city"):mark_safe(city),mark_safe("specs"):mark_safe(specs),mark_safe("date"):mark_safe(date),mark_safe('shape'):mark_safe(shape),mark_safe('duration'):mark_safe(duration)}
    return False

#one time use per csv to preevent overuse of google maps api
def CSVtoFormattedCSV(year):
    CSVreports = csv.DictReader(open('data/' + year + '.csv'))
    isWorking = 0 #counter
    with open('data/formatted'+year+'.csv', 'w') as csvfile:
        fieldnames = ['lat', 'lng','city','state','date','specs', 'shape', 'duration']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for report in CSVreports:
            print str(isWorking) + ': ' + report['City'] + ', ' + report['State']
            isWorking = isWorking + 1
            result = getData(report["City"],report["State"],report["Summary"],str.split(report["Date / Time"]," ")[0],report['Shape'],report['Duration'])
            if result != False:
                writer.writerow(result)
    print "Success!"
    #print json.dumps(data['results'][0], indent=4, sort_keys=True)
    #print reports

def getReports():
    reports = csv.DictReader(open('data/2017.csv')) #need to figure out slider interaction
    return reports

if __name__ == "__main__":
    app.debug = True
    app.run()
