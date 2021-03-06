#!/usr/bin/env python
# -*- coding: utf8
import re, math

class Position(object):
	def __init__(self, latitude, longitude, name, latlong):
		self.latitude = latitude
		self.longitude = longitude
		self.name = name
		self.latlong = latlong

s = open('positioner.txt').read()
l = []

def toDDM(deg):
   d = math.floor(deg)
   minfloat = (deg-d)*60
   return ("%d%.4f" % (d, minfloat)).replace('.', '');

for m in re.finditer('(\d{2})(\d{2})(\d{2})(\d*|)\s*/\s*(\d{2})(\d{2})(\d{2})(\d*|)\s*(.+)', s, re.MULTILINE):
	#print m.groups()
	
	# Assumes input in DDS
	#latitude = float(m.group(1)) + float(m.group(2)) / 60.0 + (float(m.group(3)) + float('0.' + m.group(4))) / 3600.0
	#longitude = float(m.group(5)) + float(m.group(6)) / 60.0 + (float(m.group(7)) + float('0.' + m.group(8))) / 3600.0

    # Assumes input in decimal degrees
	#latitude = float(m.group(1)) + float('0.' + m.group(2) + m.group(3) + m.group(4))
	#longitude = float(m.group(5)) + float('0.' + m.group(6) + m.group(7) + m.group(8))

	# Assumes input in DDM
	latitude = float(m.group(1)) + (float(m.group(2)) + float('0.' + m.group(3) + m.group(4))) / 60.0
	longitude = float(m.group(5)) + (float(m.group(6)) + float('0.' + m.group(7) + m.group(8))) / 60.0

	d = re.sub('^\s+|[\s.,]+$', '', re.sub(' {2,}', ', ', re.sub('(^|  )(\d[\d\-]*)(  |$)', '\\1\\2m\\3', m.group(9))))
	
#	decimal = '%.6f, %.6f' % (latitude, longitude)
	latlong = '%s°%s.%s\'N %s°%s.%s\'E' % (
		m.group(1), m.group(2), m.group(3) + m.group(4),
		m.group(5), m.group(6), m.group(7) + m.group(8))

#	print "%s/%s   %s" % (toDDM(latitude), toDDM(longitude), m.group(9))

	l.append(Position(latitude, longitude, d, latlong))
	
with open('normalized-mapcustomizer.txt', 'w') as f:
	for p in l:
		f.write('%.6f, %.6f {%s, %s}\n' % (p.latitude, p.longitude, p.name, p.latlong))

with open('normalized-eniro.json', 'w') as f:
	f.write('{"type": "FeatureCollection","features": [\n')
	o = []
	for p in l:
		o.append('  {"type": "Feature", "id": "%d", "geometry": {"type": "Point", "coordinates": [%f, %f]}, "properties": {"place": "%s"}}' % (
			hash((p.longitude, p.latitude)), p.longitude, p.latitude, p.name))
	f.write(',\n'.join(o))
	f.write('\n]}')

# http://cycleseven.org/gps-waypoints-routes-and-tracks-the-difference
with open('normalized.gpx', 'w') as f:
	f.write("""<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<gpx version="1.1"
    creator="positions.py"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="http://www.topografix.com/GPX/1/1"
    xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
	<metadata>
		<name>Fishing Positions</name>
	</metadata>
""")
	
	for p in l:
		f.write('<wpt lat="%.6f" lon="%.6f"><ele>0.0</ele><name>%s</name></wpt>\n' % (p.latitude, p.longitude, p.name))
	
	f.write("</gpx>")
