import googlemaps, simplekml, webbrowser
from googlemaps.geolocation import geolocate
from circle import makeCircle

#this function is what looks up the list of mac addresses and returns a location
#it actually returns a tuple consisting of (lat,long,accuracy,address)
#using geolocation and geocoding APIs
def getGoogleWiFi(macs):
	#authenticate
	gmaps = googlemaps.Client(key='YOUR_API_KEY_HERE')
	
	#feed it the mac addresses and get the result as a location object
	location_result = geolocate(gmaps, wifi_access_points=macs)
	
	#pull the pieces we need
	lat = location_result[u'location'][u'lat']
	lng = location_result[u'location'][u'lng']
	accuracy = location_result[u'accuracy']
	
	#use geocoding API to get address from lat, long
	address = gmaps.reverse_geocode((lat, lng))[0][u'formatted_address']
	pos = (lat, lng, accuracy, address)
	#return a tuple with lat, long, accuracy, address
	return pos
	
#test values if you run it directly
#go to https://developers.google.com/maps/documentation/geolocation/get-api-key
#to create a project and get an API key
#then plug it into the key= below
#after you have an API key, you go here https://console.cloud.google.com/apis/credentials to manage it


#enter from the command line or it will use the test dictionary

if __name__ == '__main__':

	choice = raw_input('Enter macs (y/n): ')
	if choice == 'y':
		raw_macs = raw_input('Enter macs separated by comma only: ').split(',')
		macs = [{'macAddress': mac} for mac in raw_macs]
			
	
	else:
		macs = [{'macAddress':'24:A4:3C:7D:BD:D0','signalStrength': -74}, \
				{'macAddress':'00:15:6D:BB:6C:BF','signalStrength': -89}, \
				{'macAddress':'24:A4:3C:7D:BD:CE','signalStrength': -90}, \
				{'macAddress':'9C:D3:6D:A0:58:1E','signalStrength': -90}, \
				{'macAddress':'24:A4:3C:DA:DA:CE','signalStrength': -91}, \
				{'macAddress':'5C:DC:96:DA:67:4A','signalStrength': -92}, \
				{'macAddress':'D0:05:2A:98:CB:F2','signalStrength': -94}]
	
	lat, lng, accuracy, address = getGoogleWiFi(macs)
	
	points = ''.join(['MAC: {}\n'.format(mac['macAddress']) for mac in macs])
	
	print points
	print u'Latitude: {}\nLongitude: {}\nAccuracy: {} meters\nAddress: {}\n'.format(lat, lng, accuracy, address)
	
	
	#create kml with the circle.py program to create a circle of the radius(accuracy)
	#then add a point in the center using just lat, long, with a name
	#save as mypoint.kml
	kml = makeCircle(lat,lng,accuracy)
	pnt = kml.newpoint()
	pnt.name = pnt.description = u'Point: ({}, {})\nPrecision: {} meters\n{}'.format(lat, lng, accuracy, address)
	pnt.coords = [(float(lng), float(lat))]
	kml.save('mypoint.kml')
	
	#open default browser with the lat/long marked
	webbrowser.open('https://www.google.com/maps/place/{},{}'.format(lat, lng), new=0, autoraise=True)
	
	
