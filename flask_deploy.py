from flask import Flask,render_template,request,jsonify
from geopy.geocoders import Nominatim
from geopy.geocoders import Photon

## create a simple flask application

app=Flask(__name__)

@app.route("/", methods=["GET"])
def welcome():
    return "Wellcome"

@app.route("/get_location", methods=["POST"])
def get_location():
    if request.method == 'POST':
        try:
            data = request.get_json()
            data = data[0]
            print(data)
            l_longitude = dict(data)['longitude']
            l_latitude = dict(data)['latitude']
            Latitude = l_latitude 
            Longitude = l_longitude
            coordinates = f"{Latitude}, {Longitude}"
            geolocator = Photon(user_agent="measurements")
            location = geolocator.reverse(coordinates, language="en")
            s_location = location.address
            l_location = location.raw['properties']['locality'] + ' ' + location.raw['properties']['district']  + ' ' + location.address
            print(location.raw)
            return l_location
        except:
            return s_location
    
if __name__=="_main__":
    app.run(debug=False)