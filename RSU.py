import pickle
import socket
import xml.etree.ElementTree as ET


HOST = "127.0.0.1"
PORT = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


# assume RSU knows route
# <route edges="-gneE36 -gneE25 gneE33"/>

class RSU(object):
    def __init__(self, route_map):
        self.route_map = route_map
        self.sendPositionRequest(self.route_map)

    def sendPositionRequest(self, route_map):
        request = "what's the position?"
        new_request = pickle.dumps(route_map)
        s.send(new_request)


#print("position is = {}".format(position))

            #s.send(request.encode())
            #data = s.recv(2048)
            #print("get position data")
            #data = pickle.loads(data)


            #new_request = "go " + edge_id + str(position)
            #new_request = route_map
# print("new_req = {}".format(new_request))
class Slot(object):
    #edge_id = E33
    # slot_no = slot_0
    def __init__(self, slot_no, edge_id, number):
        self.root = ET.parse('slot_'+number+'.xml').getroot()
        self.slot_info = {}
        #print("SLOT object edge_id = {} slot_no = {}".format(edge_id, slot_no))
        for slot_1 in self.root.findall('./' + edge_id + '/' + slot_no + '/'):

            value = slot_1.attrib
            count = 0
            for i, j in value.items():
                li = []
                if count == 1:
                    j = j[1:-1]
                    for x in j.split(","):
                        li.append(float(x))
                else:
                    li.append(j)
                self.slot_info[i] = li
                count += 1

        #print("list = {}".format(self.slot_info))

        # {'start': [-48, 55], 'pos': [-43, 68], 'speed': [2]}

"""
def fill_slot_info(self, slot_E36, edge_id):
        # assume 5 slots on E36, E25 E33
    print("edge id is {}".format(edge_id))
    for x in range(5):
        slot_E36.append(Slot("slot_" + str(x), edge_id))
    print("slot_E36={}".format(slot_E36))
"""

# E36_0(5个) --> E25_0（2个）, E25_1（3个） --> E33_0（5个）

#read to read from the route xml first to record the route
#RSU will send 1. slot info <E36_0> --- <E25_0> <E25_1>--- <E33_0> which slot including this slot's moving trajectry in list
#              2.
#'E25_0', 'E25_1'
route_1 = ['E36_0', 'E25_0', 'E25_1', 'E33_0', 'E37_0', 'E38_0']
route_2 = ['E24_0', 'E25_0', 'E33_0', 'E37_0']
route_3 = ['E25_0', 'E26_0', 'E28_0']
route_4 = ['E36_0', 'E25_0', 'E25_1', 'E33_0', 'E37_0', 'E38_0']
route_map_36 = [ {'time': ['0'], 'position': ['(-48, 55)'], 'lane': ['E36'], 'speed': ['120']},
                 {'time': ['1'], 'position': ['(-47, 57.6)'], 'lane': ['E36'], 'speed': ['120']},
                 {'time': ['2'], 'position': ['(-46, 60.2)'], 'lane': ['E36'], 'speed': ['120']},
                 ]

route = []
for i in route_1:
    route_list = []
    for y in range(5):
        slot = Slot("slot_" + str(y), i, '0')
        route_list.append(slot.slot_info)

    trajectory_E36 = []
    for x in route_list:
        route.append([i, x['position']])

for i in route_2:
    route_list = []
    for y in range(5):
        slot = Slot("slot_" + str(y), i, '1')
        route_list.append(slot.slot_info)
    #print("route_list = {}".format(route_list))

    for x in route_list:
        route.append([i, x['position']])

for i in route_3:
    route_list = []
    for y in range(5):
        slot = Slot("slot_" + str(y), i, '2')
        route_list.append(slot.slot_info)

    print("route_list = {}".format(route_list))

    for x in route_list:
        route.append([i, x['position']])

for i in route_4:
    route_list = []
    for y in range(5):
        slot = Slot("slot_" + str(y), i, '3')
        route_list.append(slot.slot_info)

    trajectory_E36 = []
    for x in route_list:
        route.append([i, x['position']])


print("route {}".format(route))


rsu = RSU(route)
