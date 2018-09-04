import os, subprocess, re
import googlemaps, simplekml, webbrowser
from googlemaps.geolocation import geolocate
from circle import makeCircle

#function to get the location based on the group of bssids/macs and their signal strengths
#remember, signal strength is optional, but will result in better accuracy
def getGoogleWiFi(macs):
	gmaps = googlemaps.Client(key='YOUR_API_KEY_HERE')

	location_result = geolocate(gmaps, wifi_access_points=macs)

	lat = location_result[u'location'][u'lat']
	lng = location_result[u'location'][u'lng']
	accuracy = location_result[u'accuracy']
	address = gmaps.reverse_geocode((lat, lng))[0][u'formatted_address']
	pos = (lat, lng, accuracy, address)
	return pos

#defining the regex to pull BSSID(mac) and signal strength(in quality percentage) from output of netsh command	
regex = 'BSSID 1                 : (.*)\r\n         Signal             : (.*)%  \r\n'

#run the netsh command and put in the data variable
data = subprocess.check_output('netsh wlan show networks mode=Bssid', shell=True)

#find all occurrences of the regex, containing bssid and signal strength
nets = re.finditer(regex, data)

#build a list of tuples, containing the bssid and the signal strength
#the conversion in there is converting the percentage into an approx RSSI in decibels

bssids = [(net.group(1), (int(net.group(2)) / 2) - 100) for net in nets]

#composing a dictionary to feed to the Google Geolocation API
macs = [{'macAddress': bssid[0], 'signalStrength': bssid[1]} for bssid in bssids]

#running the google geolocation function above to assign to variables
lat, lng, accuracy, address = getGoogleWiFi(macs)

#just putting all the bssids/macs in a block for printing out to the screen
points = ''.join(['MAC: {}\n'.format(mac['macAddress']) for mac in macs])
print points

#print the results, nicely formatted on the screen
print u'Latitude: {}\nLongitude: {}\nAccuracy: {} meters\nAddress: {}\n'.format(lat, lng, accuracy, address)

#create kml with a circle, then add a single point at the lat/long point
kml = makeCircle(lat,lng,accuracy)
pnt = kml.newpoint()
pnt.name = pnt.description = u'Point: ({}, {})\nPrecision: {} meters\n{}'.format(lat, lng, accuracy, address)
pnt.coords = [(float(lng), float(lat))]
kml.save('local_nets.kml')

#open just the lat/long point in your default web browser
webbrowser.open('https://www.google.com/maps/place/{},{}'.format(lat, lng), new=0, autoraise=True)