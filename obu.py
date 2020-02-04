import os
import sys
import optparse
import socket
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8080        # Port to listen on (non-privileged ports are > 1023)

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                          default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

# contains TraCI control loop
def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        print(step)
        det_vehs = traci.inductionloop.getLastStepVehicleIDs("det_0")
        for veh in det_vehs:
            print(veh)
            traci.vehicle.changeLane(veh, 1, 25)
        print(traci.vehicle.getIDList())
        try:
            position = traci.vehicle.getPosition("0")
            speed = traci.vehicle.getSpeed("0")
            print("position = {} speed={}".format(position, speed
                                                  ))
        except:
            continue
        if step == 500:
             traci.vehicle.changeTarget("1", "E3")
             print("here")
             #traci.vehicle.changeTarget("3", "E3")

        step += 1
    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":

    options = get_options()
    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    # traci starts sumo as a subprocess and then this script connects and runs
    #traci.start([sumoBinary, "-c", "sumo.sumocfg",
                     #"--tripinfo-output", "tripinfo.xml"])
    #run()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("get here A")
    s.bind((HOST, PORT))
    print("B = {}".format(s))
    s.listen(2)
    print("C")
    conn, addr = s.accept()
    print("get here")
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
    #s.close()


