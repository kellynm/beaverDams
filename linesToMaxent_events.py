#NOTES:
#1) sys.argv[1] must be GRASS lines vector
#2) Script must be run in EPSG: 4326 (WGS84) for Maxent formatting

import sys
import os
import grass.script as gs
from grass.pygrass.vector import Vector
from grass.pygrass import *
import sqlite3

damLines = Vector(sys.argv[1])
damLines.open(mode='r')
damLink = damLines.dblinks[0]
damAtts = damLink.table()
cursor = damAtts.execute()
lineCats = []
for row in cursor.fetchall():
    lineCats.append(row[0])

    
pointsPerline = sys.argv[2]
totalPoints = int(pointsPerline*len(lineCats))
percentIncrement = 100/int(pointsPerline)
rulesFile = open(sys.argv[0] + '/../rules.txt', mode='w')

pointID = 0
for lineCat in lineCats:
    percent = 0
    for point in range(0, int(pointsPerline)):
        ruleRow = 'P{0}{1}{0}{2}{0}{3}{4}'.format(' ', pointID, lineCat, percent,'%\n')
        rulesFile.write(ruleRow)
        percent = percent + percentIncrement
        pointID = pointID + 1



rulesFile.close()


#CREATE POINTS FROM LINE FEATURES

rules = os.path.realpath(rulesFile.name)
damPoints = sys.argv[1] + '_points'
gs.run_command('v.segment', input=sys.argv[1], output=damPoints, rules=rules, verbose='True', overwrite='True')

#add attribute table and Maxent columns
gs.run_command('v.db.addtable', map=damPoints)
gs.run_command('v.db.addcolumn', map=damPoints, columns='Species string')
                    #Add 'beaver dam occurance' in Species column for each point
gs.run_command('v.to.db', map=damPoints, type=point, option=coor, columns='Long', 'Lat')
#OUTPUT TO CSV WITH MAXENT FORMATTING
gs.run_command('db.out.ogr', input=damPoints, output=damPoints + '_maxent_input', format='CSV')












