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



#layer = sys.argv[3]

rulesFile.close()


#CREATE POINTS FROM LINE FEATURES

rules = os.path.realpath(rulesFile.name)
damPoints = sys.argv[1] + '_points'
gs.run_command('v.segment', input='kellyn_dams', output=damPoints, rules=rules, verbose='True', overwrite='True')






#POPULATE ATTRIBUTE TABLE WITH COORDINATES

#damPointsvect = Vector(damPoints)
#pointsLink = damPointsvect.dblink
#pointsAtts = pointsLink[0]


#OUTPUT TO CSV WITH MAXENT FORMATTING


