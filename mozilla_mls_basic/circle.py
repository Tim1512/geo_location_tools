import math, simplekml

#just some test values if you want to run directly
radius = 250.0 # m - the following code is an approximation that stays reasonably accurate for distances < 100km
centerLat = 42.10377 # latitude of circle center, decimal degrees
centerLon = -110.1254 # Longitude of circle center, decimal degrees

#function to return a kml object with a circle and a center point
def makeCircle(centerLat, centerLon, radius):
	
	# generate points
	N=40 #more points = more time = smoother circle
	pts = []
	for k in xrange(N + 1):

		angle = math.pi * 2 * k / N
		dx = radius * math.cos(angle)
		dy = radius * math.sin(angle)
		lat = centerLat + (180 / math.pi) * (dy / 6378137)
		lng = centerLon + (180 / math.pi) * (dx / 6378137) / math.cos(centerLat * math.pi / 180)

		pts.append((lng, lat))

	kml = simplekml.Kml() #make new kml object

	#map center point with an icon
	pnt = kml.newpoint(coords=[(centerLon, centerLat)])
	pnt.style.iconstyle.icon.href = './icons/ct2.png'

	#plot the circle points as a polygon
	pol = kml.newpolygon(name="Point Mapper", outerboundaryis=pts)
	pol.style.polystyle.color = '571400FF' #somewhat transparent red filled circle
	pol.style.polystyle.outline = 0
	pol.style.polystyle.fill = 1

	return kml #this returns a kml object, which will be saved later by the calling program

#just spew out a circle if you run it directly
if __name__ == '__main__':
	map = makeCircle(centerLat, centerLon, radius)
	map.save('circle.kml')