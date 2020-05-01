
import random
import os
import optparse
import socket
import pickle

import socket
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8080        # Port to listen on (non-privileged ports are > 1023)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)

conn, addr = s.accept()

import os, sys
# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci
import traci.constants as tc

class obu(object):
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.port = 8080

        #check options
        self.options = self.get_options()
        #check binary
        self.check_binary(self.options)

        data_ = conn.recv(4096)
        data = pickle.loads(data_)

        print("data = {}".format(data))

        if not data:
            return

        traci.start([self.sumoBinary, "-c", "sumo.sumocfg",
                     "--tripinfo-output", "tripinfo.xml"])

        self.run(data)


    def get_options(self):
        opt_parser = optparse.OptionParser()
        opt_parser.add_option("--nogui", action="store_true",
                              default=False, help="run the commandline version of sumo")
        options, args = opt_parser.parse_args()
        return options

    def check_binary(self, option):
        if option.nogui:
            self.sumoBinary = checkBinary('sumo')
            print("A")

        else:
            self.sumoBinary = checkBinary('sumo-gui')
            print("B")


    def run(self, route_map):

        step = 0
        print("start here route map length {}".format(len(route_map)))

        l_0 = route_map[:30]
        l_1 = route_map[30:50]
        l_2 = route_map[50:65]
        l_3 = route_map[65:]

        print("l2 = {}".format(l_2))
        traci.simulationStep()

        while traci.simulation.getMinExpectedNumber() > 0 and step < 30:

            print("start sumo")
            if step < 30:
                info0 = l_0[step]
                x0, y0 = float(info0[1][0][1:-1].split(',')[0]), float(info0[1][0][1:-1].split(',')[1])
                edge_ID_0 = info0[0][:3]

                if step < 15:
                    info1 = l_1[step]
                    info2 = l_2[step]

                    x1, y1 = float(info1[1][0][1:-1].split(',')[0]), float(info1[1][0][1:-1].split(',')[1])
                    x2, y2 = float(info2[1][0][1:-1].split(',')[0]), float(info2[1][0][1:-1].split(',')[1])

                    edge_ID_1 = info1[0][:3]
                    edge_ID_2 = info2[0][:3]

                elif 15 <= step < 20:
                    info1 = l_1[step]
                    x1, y1 = float(info1[1][0][1:-1].split(',')[0]), float(info1[1][0][1:-1].split(',')[1])
            """
            elif step >= 30:
                info3 = l_3[step-30]
                x3, y3 = float(info3[1][0][1:-1].split(',')[0]), float(info3[1][0][1:-1].split(',')[1])
                edge_ID_3 = info3[0][:3]
            """

            def moveVeh(edge_ID, id, x,y, info):
                if edge_ID == 'E33':
                    print("going on E33")
                    traci.vehicle.moveToXY(id, 'gne' + edge_ID, 0, x, y, 115, 1)
                    print("veh={} speed={}".format(id, traci.vehicle.getSpeed(id)))
                elif edge_ID == 'E25':
                    print("going on E25")
                    if info[0][3:] == "_1":
                        if route_map.index(info) == 10:
                            traci.vehicle.changeLane(id, 1, 4000.00)
                            print("veh={} speed={}".format(id, traci.vehicle.getSpeed(id)))
                        elif step == 14:
                            traci.vehicle.changeLane(id, 0, 1000.00)
                        else:
                            print("veh={} speed={}".format(id, traci.vehicle.getSpeed(id)))
                            pass
                    else:
                        traci.vehicle.moveToXY(id, '-gne' + edge_ID, 0, x, y, 90, 1)
                        print("veh={} speed={}".format(id, traci.vehicle.getSpeed(id)))

                elif edge_ID == 'E36':
                    print("id list = {}".format(traci.vehicle.getIDList()))
                    print("going on E36")
                    traci.vehicle.moveToXY(id, '-gne' + edge_ID, 0, x, y, 30, 1)
                    print("veh={} speed={}".format(id, traci.vehicle.getSpeed(id)))
                elif edge_ID == 'E24':
                    print("going on E24")
                    traci.vehicle.moveToXY(id, '-gne' + edge_ID, 0, x, y, 118, 1)
                    print("veh={} speed={}".format(id, traci.vehicle.getSpeed(id)))

                elif edge_ID == 'E26':
                    print("going on E26")
                    traci.vehicle.moveToXY(id, '-gne' + edge_ID, 0, x, y, 90, 1)

                elif edge_ID == 'E28':
                    print("going on E28")
                    traci.vehicle.moveToXY(id, '-gne' + edge_ID, 0, x, y, 90, 1)
                elif edge_ID == 'E37':
                    print("going on E37")
                    traci.vehicle.moveToXY(id, 'gne' + edge_ID, 0, x, y, 100, 1)

                elif edge_ID == 'E38':
                    print("going on E38")
                    traci.vehicle.moveToXY(id, '-gne' + edge_ID, 0, x, y, 35, 1)
            #
            if step< 30:
                print("step < 30")
                moveVeh(edge_ID_0, '0', x0, y0, info0)
                if step < 15:
                    moveVeh(edge_ID_1, '1', x1, y1, info1)
                    moveVeh(edge_ID_2, '2', x2, y2, info2)
                elif step > 15:
                    moveVeh(edge_ID_1, '1', x1, y1, info1)
            """
            elif step>=30:
                print("step >= 30")
                moveVeh(edge_ID_3, '3', x3, y3, info3)
            """


            print("vehicle{} description {}".format(id, traci.vehicle.getSubscriptionResults(id)))
            traci.simulationStep()

            step += 1
            print("step = {}".format(step))
            print("ID list = {}".format(traci.vehicle.getIDList()))

        traci.close()
        sys.stdout.flush()


obu = obu()

