from flask import Flask, render_template
import urllib2, json
from django.utils.safestring import mark_safe

app = Flask(__name__)
key = "AIzaSyCribAPQyNvWFjOt0g66YjJVP_q2REPvoE"

#format City name for querey
def formatCity(name):
    ans = str.split(name)
    return "+".join(ans)


@app.route("/")
def root():
    #SUPER IMPORTANT FOR FORMATTING
    CSVdata = [["New York","NY","saw a potato fly overhead"]]
    reports = [] #list of lists of formatted reports [latitude,longitude,state,city,specs]
    for report in CSVdata:
        reports.append(getData(report[0],report[1],report[2]))
    #print json.dumps(data['results'][0], indent=4, sort_keys=True)
    print reports
    return render_template("d3test.html", reports=mark_safe(reports)) #reports is a list of lists [[latitude,longitude,state,city,specs]

def getData(city,state,specs): #reutrns [latitude,longitude,state,city,specs]  where specs are the extra details about the report
    city = formatCity(city)
    u = urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address="+city+",+"+state+"&key="+key)
    response = u.read()
    data = json.loads( response )
    return [data['results'][0]['geometry']['location']['lat'],-1*data['results'][0]['geometry']['location']['lng'],mark_safe(state),mark_safe(city),mark_safe(specs)]

if __name__ == "__main__":
   app.debug = True
   app.run()
