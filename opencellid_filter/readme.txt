Get the opencellid CSV database here: https://unwiredlabs.com/dashboard?ref=opencellid#downloads
Or go here and login and download: https://opencellid.org/

It's about 900MB today, zipped in gz format. Unzipped it's too big to open in excel, so hence, this filter.

You'll need QT4 installed for python27. Get it here for windows: https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/

The rest of the libraries can be installed with pip or the equivalent repo version for your distro.

You'll need:

django
simplekml
geopy


If you're on debian/ubuntu/mint, you should be able to sudo apt install python-qt4


Converting the entire CSV file into a SQLite db takes a while. Be patient.

Also, you may want to export some dbs for your country or for separate carriers.

That will make subsequent filtering faster.


