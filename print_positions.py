import traci
import traci.constants as tc
import pyproj

PORT = 8813

traci.init(PORT) 


vehID = 'veh1'
traci.vehicle.subscribe(vehID, (tc.VAR_SPEED, tc.VAR_POSITION))

print traci.vehicle.getSubscriptionResults(vehID)
for step in range(100):
   print "step", step
   traci.simulationStep()
   r = traci.vehicle.getSubscriptionResults(vehID)
   print r
   x = r[tc.VAR_POSITION][0]
   y = r[tc.VAR_POSITION][1]
   lon, lat = traci.simulation.convertGeo(x, y)
   s = r[tc.VAR_SPEED]
   print lat, lon 

traci.close()
