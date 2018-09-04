import googlemaps

lat, lng = 40.663749, -111.497065

gmaps = googlemaps.Client(key='YOUR_API_KEY_HERE')

addresses = gmaps.reverse_geocode((lat, lng))

#result returns a list of hits

print 'Geocoding {}, {} into an address...'.format(lat,lng)
print addresses[0][u'formatted_address']
