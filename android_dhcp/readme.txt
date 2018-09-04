Android typically keep some of their DHCP lease records in /data/misc/dhcp.

Most Androids only keep the last one or maybe a couple of them, but Samsung keeps up to ten and LG will keep a few dozen. The most I've seen is 56.

You'll need:

python2.7
pygle - and modifying the network.py in your site-packages/pygle folder, changing "first=" to "searchAfter=".
		Also, you have to get an API username and API password from api.wigle.net and enter those creds in the config.py for pygle
		
