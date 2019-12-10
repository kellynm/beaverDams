#NOTES:
#1) sys.argv[1] must be GRASS lines vector
#2) Script must be run in GRASS mapset with EPSG: 4326 (WGS84) for Maxent formatting

import sys
import os
import grass.script as gs
from grass.pygrass.vector import Vector
from grass.pygrass import *
import sqlite3
import csv

try:
    damsIn = sys.argv[1]
    pointsPerline = sys.argv[2]
    csvOutputdir = sys.argv[3]
    
except IndexError:
    print("Please ensure all required parameters are given and follow the format: <linesVectorInput> <pointsPerline> <csvOutputdirectory>")
    sys.exit()

damLines = Vector(damsIn)
damLines.open(mode='r')
damLink = damLines.dblinks[0]
damAtts = damLink.table()
cursor = damAtts.execute()
lineCats = []
for row in cursor.fetchall():
    lineCats.append(row[0])

    

totalPoints = int(pointsPerline*len(lineCats))
percentIncrement = 100/int(pointsPerline)
rulesFile = open(sys.argv[3] + '/rules.txt', mode='w')

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
damPoints = damsIn + '_points'
if len(sys.argv) >= 5:
    studyRegion = sys.argv[4]
    gs.run_command('g.region', vector=studyRegion)
else: 
    pass
gs.run_command('v.segment', input=damsIn, output=damPoints, rules=rules, verbose='True', overwrite='True')

#add attribute table and Maxent columns
gs.run_command('v.db.addtable', map=damPoints)
gs.run_command('v.to.db', map=damPoints, type='point', option='coor', columns='Long,Lat')

points = Vector(damPoints)
points.open(mode='r')
pointsLink = points.dblinks[0]
pointsAtts = pointsLink.table()
cursor_2 = pointsAtts.execute()


#OUTPUT TO CSV WITH MAXENT FORMATTING
csvOutputdir = sys.argv[3]
csvOutputFile = os.path.join(csvOutputdir, damPoints + '_maxent_input.csv')

gs.run_command('db.out.ogr', input=damPoints, output=csvOutputFile, format='CSV', overwrite='True') 














