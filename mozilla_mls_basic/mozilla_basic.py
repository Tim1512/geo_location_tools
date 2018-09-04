import requests, json, webbrowser
from circle import makeCircle #this is just a little python routine to create a circle as a polygon in kml

#address url for posting
uri = 'https://location.services.mozilla.com/v1/geolocate?key=test'

#data to be posted to above url
data = '{"wifiAccessPoints": \
		[{"macAddress": "58:B6:33:1E:61:08"},\
		{"macAddress": "58:B6:33:1E:61:0C"},\
		{"macAddress": "58:B6:33:1E:F7:A8"}]}'

#actually do the POST action		
r = requests.post(uri, data=data)

#pull in the data, which is serialized json and parse it
loc = json.loads(r.text)
lat = loc.get('location')['lat']
lng = loc.get('location')['lng']
accuracy = loc.get('accuracy')

#just print them out
print 'Latitude: {}\nLongitude: {}\nAccuracy: {}'.format(lat, lng, accuracy)


#create kml containing the single point
kml = makeCircle(lat,lng,accuracy)
pnt = kml.newpoint()
pnt.name = pnt.description = u'Point: ({}, {})\nPrecision: {} meters'.format(lat, lng, accuracy)
#points are just strings, so making sure they are floats here
pnt.coords = [(float(lng), float(lat))]
kml.save('mozilla_point.kml')

#if you open this url with the points appended in lat, long format, it will open a google maps page in your default browser
webbrowser.open('https://www.google.com/maps/place/{},{}'.format(lat, lng), new=0, autoraise=True)
