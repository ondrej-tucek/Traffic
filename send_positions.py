import sys, traci, requests, json
import traci.constants as tc


PORT = 8813

traci.init(PORT) 
URLS = {
#'veh1': 'http://api-m2x.att.com/v2/devices/04d1817839978781cc29eee729c03d6f',
'veh2': 'http://api-m2x.att.com/v2/devices/1435efca54872bf96e5232fbcd670792',
'veh3': 'http://api-m2x.att.com/v2/devices/f6792062cb048eeeaa5c3b3079d70e82',
'veh4': 'http://api-m2x.att.com/v2/devices/a2ca89cef728499d5d0a299553db4f71',
'veh5': 'http://api-m2x.att.com/v2/devices/6c0bf369abd9d920ddd8a85801944429',
'veh6': 'http://api-m2x.att.com/v2/devices/1dcd9af8e1fea96903ba5a1f9ec1ae3b',
'veh7': 'http://api-m2x.att.com/v2/devices/c2181b6165f7db6055bea53b7938fd60',
'veh8': 'http://api-m2x.att.com/v2/devices/9a5bc79f86eedc092c86c09f4908c806',
'veh9': 'http://api-m2x.att.com/v2/devices/cfa068e9d790388c2eb3d8839ca18b17',
'veh10': 'http://api-m2x.att.com/v2/devices/de34e99d49cf8b36c5f23b9d7411d414',
'veh11': 'http://api-m2x.att.com/v2/devices/3e9acead0a8584f99ed3aef0e41a14d5'
}

SESSIONS = {}

vehicles = URLS.keys()
for vehicle in vehicles:
#    traci.vehicle.subscribe(vehicle, (tc.VAR_SPEED, tc.VAR_POSITION))
    SESSIONS[vehicle] = requests.Session()
    SESSIONS[vehicle].headers.update({
        'X-M2X-KEY' : 'efb3f8f7e6b8ab15367d566660112d25',
        'Content-Type' : 'application/json'
        })
    print repr(SESSIONS[vehicle])
    print len(SESSIONS)
    print

for step in range(1): # headstart
    traci.simulationStep(500)

known = []

for step in range(int(sys.argv[1])):
    print "step", step
#    for vehicle in vehicles:
    for vehicle in set(traci.vehicle.getIDList()).intersection(vehicles):
        print("Vehicle: %s"%vehicle)
        try:
            # traci.vehicle.subscribe(vehicle, (tc.VAR_SPEED, tc.VAR_POSITION))
            # r = traci.vehicle.getSubscriptionResults(vehicle)
            # print r
            # x = r[tc.VAR_POSITION][0]
            # y = r[tc.VAR_POSITION][1]
            x,y = traci.vehicle.getPosition(vehicle)
            lon, lat = traci.simulation.convertGeo(x, y)
#            s = r[tc.VAR_SPEED]
            print lat, lon
            
            r = SESSIONS[vehicle].put(URLS[vehicle]+'/location', json.dumps({'longitude': lon, 'latitude': lat}))
            print("Session result: %s\n"%r)
            if not vehicle in known:
                known.add(vehicle)
        except Exception, e:
            if vehicle in known:
                print("The car %s just left. Bye bye."%vehicle)
                vehicles.remove(vehicle)
                SESSIONS[vehicle].close()
    traci.simulationStep()

traci.close()
