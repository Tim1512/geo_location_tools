#just dumps the packages from an android phone with USB debugging (ADB) turned on
#adb must be in your path

from subprocess import check_output
import re, csv

data = str(check_output('adb shell "dumpsys package"', shell=True))

regex = 'Package \\[(.*?)\\] \\((.*?)\\):\r?\n    userId=(.*?)\r?\n'

results = re.finditer(regex, data)
packages = [(x.group(3).zfill(5), x.group(1), x.group(2)) for x in results]
packages.sort()

with open('packages_android.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerow(('userID','packageName','someID'))
	for package in packages:
		writer.writerow(package)
		

