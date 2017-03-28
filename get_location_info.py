from flask import Flask, render_template
import urllib2, json

app = Flask(__name__)
key = "AIzaSyCribAPQyNvWFjOt0g66YjJVP_q2REPvoE"

#format City name for querey
def formatCity(name):
    ans = str.split(name)
    return "+".join(ans)


@app.route("/info")
def root():
    city = formatCity("New York")
    state = "NY"
    u = urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address="+city+",+"+state+"&key="+key)
    response = u.read()
    data = json.loads( response )
    #print json.dumps(data['results'][0], indent=4, sort_keys=True)
    return render_template("get_location_info.html", status = data['status'], location=data['results'][0]['address_components'][0]['long_name'],latitude = data['results'][0]['geometry']['location']['lat'],longitude=data['results'][0]['geometry']['location']['lng'])


if __name__ == "__main__":
   app.debug = True
   app.run()
