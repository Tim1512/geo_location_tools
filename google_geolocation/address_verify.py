#go to https://developers.google.com/maps/documentation/geolocation/get-api-key
#to create a project and get an API key
#then plug it into the key= below
#after you have an API key, you go here https://console.cloud.google.com/apis/credentials to manage it



#if this isn't installed, install with pip "pip install googlemaps"
import googlemaps

#you need a google geolocation API key... free
gmaps = googlemaps.Client(key='YOUR_API_KEY')

#just the list of addresses, hard-coded
addresses = ['123 Fake Street, Anytown, USA 12345', '456 Other Street, Otherton, USA 54321']

#for each address in the list, find its geo information
geocodings = [gmaps.geocode(address) for address in addresses]

#each hit is actually a list of hits, which accounts for similarly-named locations
#if you have a specific location, it's just gonna be a list of one item
for geo in geocodings:
	for loc in geo:
		lat = loc[u'geometry'][u'location'][u'lat']
		lon = loc[u'geometry'][u'location'][u'lng']
		add = loc[u'formatted_address']
		
		print 'Address: {}\nLatitude: {}\nLongitude: {}\n'.format(add, lat, lon)

		
