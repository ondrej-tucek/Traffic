import sys, traci, requests, json
import traci.constants as tc


PORT = 8813

traci.init(PORT) 
URLS = {
'veh1': 'http://api-m2x.att.com/v2/devices/04d1817839978781cc29eee729c03d6f/location'
}

SESSIONS = {}

vehicles = URLS.keys()
for vehicle in vehicles:
    traci.vehicle.subscribe(vehicle, (tc.VAR_SPEED, tc.VAR_POSITION))
    SESSIONS[vehicle] = requests.Session()
    SESSIONS[vehicle].headers.update({
        'X-M2X-KEY' : 'efb3f8f7e6b8ab15367d566660112d25',
        'Content-Type' : 'application/json'
        })
    print repr(SESSIONS[vehicle])

    for step in range(20):
        traci.simulationStep()

        for step in range(int(sys.argv[1])):
            print "step", step
            traci.simulationStep()
            for vehicle in vehicles:
                print("Vehicle: %s"%vehicle)
                r = traci.vehicle.getSubscriptionResults(vehicle)
                if r:
                    print r
                    x = r[tc.VAR_POSITION][0]
                    y = r[tc.VAR_POSITION][1]
                    lon, lat = traci.simulation.convertGeo(x, y)
                    s = r[tc.VAR_SPEED]
                    print lat, lon
                    
                    r = SESSIONS[vehicle].put(URLS[vehicle], json.dumps({'longitude': lon, 'latitude': lat}))
                    print("Session result: %s\n"%r)
                else:
                    print("The car %s just left. Bye bye."%s)
                    vehicles.remove(vehicle)
                    SESSIONS[vehicle].close()

                    traci.close()
