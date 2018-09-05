#for this to work, you need android debug bridge in your path and USB debugging turned on on your device
#adb shell commands will always return \n on linux, \r\n on Windows, so I'll strip out the \r in the outputs
#if you run on linux/mac, the \r won't be there, so it won't matter

import os, subprocess
#make folder to hold the separate files
os.mkdir('dumpsys_files')

#dump the whole dumpsys command into one file first, removes carriage returns for Windows systems
with open('./dumpsys_files/dumpsys.txt', 'wb') as f:
	dumpsys_data = subprocess.check_output('adb shell dumpsys', shell=True).replace('\r', '')
	f.write(dumpsys_data)
	
#this just gets the list (-l) of services
svc_raw = subprocess.check_output('adb shell dumpsys -l', shell=True)

#each line in the file (except the title line) starts with two spaces. If your device does it differently, change the startswith thing
services = [line.strip() for line in svc_raw.split('\n') if line.startswith('  ')]

#loop through the list of services, create file for each in the output directory
for service in services:
	with open('./dumpsys_files/{}.txt'.format(service), 'wb') as f:
		#run the dumpsys function for each service individually, replacing \r (CR) if you're on Windows
		file_data = subprocess.check_output('adb shell dumpsys {}'.format(service), shell=True).replace('\r', '')
		f.write(file_data)
