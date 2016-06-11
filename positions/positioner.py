#!/usr/bin/env python
# -*- coding: utf8
import re

class Position(object):
	def __init__(self, latitude, longitude, name, latlong):
		self.latitude = latitude
		self.longitude = longitude
		self.name = name
		self.latlong = latlong

s = open('positioner.txt').read()
l = []

for m in re.finditer('(\d{2})(\d{2})(\d{2})(\d*|)\s*/\s*(\d{2})(\d{2})(\d{2})(\d*|)\s*(.+)', s, re.MULTILINE):
	print m.group(4)
	
	# Assumes input in DDS
	#latitude = float(m.group(1)) + float(m.group(2)) / 60.0 + (float(m.group(3)) + float('0.' + m.group(4))) / 3600.0
	#longitude = float(m.group(5)) + float(m.group(6)) / 60.0 + (float(m.group(7)) + float('0.' + m.group(8))) / 3600.0

	# Assumes input in DDM
	latitude = float(m.group(1)) + (float(m.group(2)) + float('0.' + m.group(3) + m.group(4))) / 60.0
	longitude = float(m.group(5)) + (float(m.group(6)) + float('0.' + m.group(7) + m.group(8))) / 60.0

	d = re.sub('^\s+|[\s.,]+$', '', re.sub(' {2,}', ', ', re.sub('(^|  )(\d[\d\-]*)(  |$)', '\\1\\2m\\3', m.group(9))))
	
#	decimal = '%.6f, %.6f' % (latitude, longitude)
	latlong = '%s°%s.%s\'N %s°%s.%s\'E' % (
		m.group(1), m.group(2), m.group(3) + m.group(4),
		m.group(5), m.group(6), m.group(7) + m.group(8))

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

with open('normalized.gpx', 'w') as f:
	f.write("""<?xml version="1.0" encoding="UTF-8"?>\n<gpx version="1.0">\n<name>Westcoast Fishing Positions</name>\n""")
	for p in l:
		f.write('<wpt lat="%.6f" lon="%.6f"><name>%s</name></wpt>\n' % (p.latitude, p.longitude, p.name))
	f.write("</gpx>")
