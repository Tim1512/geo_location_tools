#the pygle library has to be modified a bit, since it hasn't kept up with API changes
#in the site packages folder, find the network.py file and find the "first=" and change
#it to "searchAfter="
#then, go get an account on wigle, go to https://api.wigle.net/ and follow the instructions
#you will have to enter your api username (not regular user) and your api password (not regular password)
#in the pygle config.py file

#note: wigle uses openstreetmaps for their geocoding on the backend, so... there you go



import os
from pygle import config, network
from datetime import datetime as dt

#open list to hold macs and get bssids from filenames
#convert timestamps and such (they will be UTC, BTW)
macs = []
for file in os.listdir('.'):
	if file.endswith('lease2'):
		mod_utc = str(dt.fromtimestamp(os.path.getmtime(file)))
		mac = file[13:30].replace('_', ':')
		macs.append((mac, mod_utc))

#make a list to hold the info you'll get from wigle network search		
net_data = []		
for mac in macs:
	data = network.search(netid=mac) #this is a simple search by bssid, which should be unique
	net_data.append(data)

#just write a csv out with what we can get
#you could also run these lat/long/addresses against google geocoding also	
with open('results.csv', 'wb') as f:
	f.write('ssid,bssid,lat,lng,lasttime,country,region,city,house_number,road\n')
	for item in net_data:
		if item.get(u'resultCount') != 0:
			net = item[u'results'][0]
			ssid = net.get(u'ssid', 'None')
			bssid = net.get(u'netid', 'None')
			lat =  net.get(u'trilat', '0.0')
			lng = net.get(u'trilong', '0.0')
			lasttime = net.get(u'lasttime', 'None')
			country = net.get(u'country', 'None')
			region = net.get(u'region', 'None')
			city = net.get(u'city', 'None')
			house_number = net.get(u'housenumber', 'None')
			road = net.get(u'road', 'None')
			f.write('{},{},{},{},{},{},{},{},{},{}\n'.\
			format(ssid,bssid,lat,lng,lasttime,country,region,city,house_number,road))
