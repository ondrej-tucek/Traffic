import traci
import traci.constants as tc
import pyproj

PORT = 8813

#taken from osm.net.xml
#    <location netOffset="-390665.61,-5820288.44" convBoundary="0.00,0.00,2745.71,2424.95" origBoundary="13.388361,52.522056,13.428613,52.544043" projParameter="+proj=utm +zone=33 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"/>

OFFSET_x = -390665.61
OFFSET_y = -5820288.44
PROJECTION = pyproj.Proj("+proj=utm +zone=33 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

def transform(x,y):
	return PROJECTION(x + OFFSET_x, y + OFFSET_y, inverse=True)

traci.init(PORT) 


vehID = 'veh1'
traci.vehicle.subscribe(vehID, (tc.VAR_SPEED, tc.VAR_POSITION))

print traci.vehicle.getSubscriptionResults(vehID)
for step in range(3):
   print "step", step
   traci.simulationStep()
   r = traci.vehicle.getSubscriptionResults(vehID)
   print r
   print transform(r[tc.VAR_POSITION][0], r[tc.VAR_POSITION][1])

traci.close()
