import sys, sqlite3, csv, os, simplekml, zipfile
from geopy.geocoders import Nominatim
from PyQt4 import QtCore, QtGui, uic
from PyQt4.Qt import QMessageBox
from subprocess import Popen
from django.utils.encoding import smart_unicode

qtCreatorFile = "./ui/OpenCellIDFilter.ui" # Enter User Interface file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class OpenCellId(QtGui.QMainWindow, Ui_MainWindow):
	
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		#Exit Actions
		self.actionExit.triggered.connect(QtGui.qApp.quit)
		#Select CSV File for import
		self.actionImport.triggered.connect(self.importFileSelect)
		self.select_csv_button.clicked.connect(self.importFileSelect)
		#Select SQLite file for export
		self.actionExport.triggered.connect(self.exportFileSelect)
		self.select_sql_export_button.clicked.connect(self.exportFileSelect)
		#Initiate import-export action (CSV2SQLite)
		self.import_button.clicked.connect(self.exportSQLite)
		#Select SQLite input file for filtering
		self.select_sql_source_button.clicked.connect(self.filterSelectFile)
		#Exporting filtered files
		self.export_button.clicked.connect(self.filterOutput)
		#search Nominatim for Bounding Box
		self.bb_nominatim_button.clicked.connect(self.bbNominatim)
		self.show_bounding_box.clicked.connect(self.showBoundingBox)

	def showBoundingBox(self):
		if (self.lat1_input.text() != "" and self.lat2_input.text() != ""\
			and self.long1_input.text() != "" and self.long2_input.text() != ""):
			kml = simplekml.Kml()
			b_box = kml.newgroundoverlay (name=smart_unicode(self.bounding_box_entry.text()))
			b_box.color = '371400FF' #this is transparent red
			b_box.latlonbox.north = float(self.lat2_input.text())
			b_box.latlonbox.south = float(self.lat1_input.text())
			b_box.latlonbox.east = float(self.long2_input.text())
			b_box.latlonbox.west = float(self.long1_input.text())
			
			#save kml file with name based on the full location name
			kml_filename = smart_unicode(self.bounding_box_entry.text()).replace(', ', '-').replace(' ', '_') + '_bounding_box.kml'
			kml.save (kml_filename)
			Popen('"C:/Program Files (x86)/Google/Google Earth Pro/client/googleearth.exe" "{}"'.format(kml_filename), stdin=None, stdout=None, stderr=None, close_fds=True, shell=True)
		else:
			self.popupWindow("No Coordinates For Box", "You are missing one or more coordinates for your bounding box. Try searching a location to populate lat/long values.")
		
			
		
	def importFileSelect(self):
		import_name = QtGui.QFileDialog.getOpenFileName()
		if import_name != "":
			self.file_import_box.setText(import_name)

	def exportFileSelect(self):
		export_name = QtGui.QFileDialog.getSaveFileName()
		if export_name != "":
			self.file_export_box.setText(export_name)
				
	def exportSQLite(self):
		db_filename = str(self.file_export_box.text().toUtf8())
		if os.path.isfile(db_filename):
			os.remove(db_filename)
		
		csv_filename = str(self.file_import_box.text().toUtf8())

		con = sqlite3.Connection(db_filename)
		cur = con.cursor()
		cur.execute('CREATE TABLE "towers" ("radio" varchar(12), "mcc" varchar(12), "net" varchar(12),"area" varchar(12),"cell" varchar(12),"unit" varchar(12),"lon" varchar(12),"lat" varchar(12),"range" varchar(12),"samples" varchar(12),"changeable" varchar(12),"created" varchar(12),"updated" varchar(12),"averageSignal" varchar(12));')
		
		input_file = open(csv_filename)
		check = input_file.readline()
		if check.split(',')[0] != "radio":
			input_file.seek(0)
		csv_reader = csv.reader(input_file, delimiter = ',')
		cur.executemany('INSERT INTO towers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', csv_reader)
		
		cur.close()
		con.commit()
		con.close()
		input_file.close()
		#just let the user know the file was created successfully
		self.popupWindow('Successful Conversion', 'File successfully converted to SQLite  ')
		
	def popupWindow(self, title, message):
		self.msg = QMessageBox()
		self.msg.setIcon(QMessageBox.Information)
		self.msg.setWindowTitle(title)
		self.msg.setText(message)
		self.msg.setStandardButtons(QMessageBox.Ok)
		self.msg.exec_()

		
	def filterSelectFile(self):
		filter_input_file = str(QtGui.QFileDialog.getOpenFileName())
		if filter_input_file != "":
			self.source_SQLite_box.setText(filter_input_file)
			
	def filterOutput(self):
		
		output_base = str(QtGui.QFileDialog.getSaveFileName())
		count = 0
		
		CREATE_SQLITE = False
		CREATE_KMZ = False
		CREATE_CSV = False
		
		if self.export_sqlite_check.isChecked():
			CREATE_SQLITE = True
			
			if os.path.isfile('output_base' + '.db'):
				self.popupWindow("SQLite Database already exists", "This file exist already. This will append to the current DB, adding the table if necessary.")
			output_con = sqlite3.Connection(output_base + '.db')
			output_cur = output_con.cursor()
			output_cur.execute('CREATE TABLE IF NOT EXISTS "towers" ("radio" varchar(12), "mcc" varchar(12), "net" varchar(12),"area" varchar(12),"cell" varchar(12),"unit" varchar(12),"lon" varchar(12),"lat" varchar(12),"range" varchar(12),"samples" varchar(12),"changeable" varchar(12),"created" varchar(12),"updated" varchar(12),"averageSignal" varchar(12));')

		
		if self.export_kmz_check.isChecked():
			CREATE_KMZ = True
			if os.path.isfile(output_base + '.kmz'):
				self.popupWindow('Already Existing File', 'The KMZ file already exists. Will replace.')
				os.remove(output_base + '.kmz')
			kml = simplekml.Kml()
		
		if self.export_csv_check.isChecked():
			CREATE_CSV = True
			csv_file = open(output_base + '.csv', 'wb')
			writer = csv.writer(csv_file, delimiter = ',')
			writer.writerow(('radio','mcc','net','area','cell','unit','lon','lat','range','samples','changeable','created','updated','averageSignal'))		
		
		
		#read lat/long values and get them in the proper order
		try:
			lat1 = float(self.lat1_input.text().toUtf8())
			lat2 = float(self.lat2_input.text().toUtf8())
			long1 = float(self.long1_input.text().toUtf8())
			long2 = float(self.long2_input.text().toUtf8())
			
			if max(lat1,lat2) == max(abs(lat1),abs(lat2)):
				pass
			else:
				lat1,lat2 = lat2,lat1
			if max (long1,long2) == max(abs(long1),abs(long2)):
				pass
			else:
				long1,long2 = long2,long1
			if lat1 != '' and lat2 != '' and long1 != '' and long2 != '':
				loc_string = ' AND lat BETWEEN {a} AND {b} AND lon BETWEEN {c} AND {d}'.format(a=lat1,b=lat2,c=long1,d=long2)
			else:
				loc_string = ''
		except ValueError:
			lat1, lat2, long1, long2 = '','','',''
			loc_string = ''
			
		
		if self.MCC_input.text().toUtf8() == "":
			mob_cc = ' LIKE "%"'
		else:
			mob_cc = '={a}'.format(a=self.MCC_input.text().toUtf8())
		if self.MNC_input.text().toUtf8() == "":
			mnc = ' LIKE "%"'
		else:
			mnc = '={a}'.format(a=self.MNC_input.text().toUtf8())
		if self.LAC_input.text().toUtf8() == "":
			lac = ' LIKE "%"'
		else:
			lac = '={a}'.format(a=self.LAC_input.text().toUtf8())
		if self.CID_input.text().toUtf8() == "":
			cid = ' LIKE "%"'
		else:
			cid = '={a}'.format(a=self.CID_input.text().toUtf8())
		

		input_con = sqlite3.Connection(str(self.source_SQLite_box.text().toUtf8()))
		input_cur = input_con.cursor()
		query = 'SELECT * FROM towers WHERE mcc{a} AND net{b} AND area{c} AND cell{d}{e};'.format(a=mob_cc, b=mnc, c=lac, d=cid, e=loc_string)
		input_cur.execute(query)
		
		def ResultIter(cursor, array_size=5000):
    
			while True:
				results = cursor.fetchmany(array_size)
				if not results:
					break
				for result in results:
					yield result
		
		for result in ResultIter(input_cur):
			
		
			if CREATE_SQLITE:

				output_cur.executemany('INSERT INTO towers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (result,))
			
			if CREATE_KMZ:
				
				desc = '{a}:{b}:{c}:{d}'.format(a=result[1], b=result[2], c=result[3], d=result[4])
				nm = desc #'CID: {a}'.format(a=result[4])
				pnt = kml.newpoint(name = nm, description = desc, coords = \
				[(float(result[6]), float(result[7]))])
				pnt.style.iconstyle.icon.href = 'greentower.png'

		
			if CREATE_CSV:
				writer.writerow(result)
		
		if CREATE_SQLITE:
			count += 1
			output_con.commit()
			output_con.close()

		if CREATE_CSV:
			count += 1
			csv_file.close()
		
		if CREATE_KMZ:
			count += 1
			kml.save('doc.kml')
			zf = zipfile.ZipFile(output_base + '.kmz', 'a')
			zf.write('doc.kml')
			zf.write('greentower.png')
			os.remove('doc.kml')
			zf.close()
			if os.path.getsize(output_base + '.kmz') > 10000000:
				self.popupWindow('Enormous KMZ file', 'Your KMZ file is enormous. Google Earth may have problems opening it in a reasonable fashion.')
			if self.open_earth_button.isChecked():
				Popen('"C:\Program Files (x86)\Google\Google Earth Pro\client\googleearth.exe" "{}"'.format(output_base + '.kmz'), stdin=None, stdout=None, stderr=None, close_fds=True)

		if count == 0:
			self.popupWindow('Unsuccessful', 'No files were exported')
		else:
			self.popupWindow('Successful File Exports', str(count) + ' files were exported.  ')
		
		input_con.close()

	def bbNominatim(self):
		geolocator = Nominatim()
		location_name = self.bounding_box_entry.text().toUtf8()
		location = geolocator.geocode(location_name, language = 'en')
		try:
			geo_box = location.raw[u'boundingbox']
			self.lat1_input.setText (geo_box[0].encode('utf-8'))
			self.lat2_input.setText (geo_box[1].encode('utf-8'))
			self.long1_input.setText (geo_box[2].encode('utf-8'))
			self.long2_input.setText (geo_box[3].encode('utf-8'))
			self.bounding_box_entry.setText(smart_unicode(location.raw[u'display_name']))
		except AttributeError:
			self.bounding_box_entry.setText('''No location found. Maybe it's you.''')
			self.popupWindow('Location Not Found', '''I can't find that location. Maybe you can try going back in time and learning how to spell.''')
			

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = OpenCellId()
    window.show()
    sys.exit(app.exec_())