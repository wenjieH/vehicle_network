import random

from Parameters import CommunicationRange, MaxValue, Max_layer, Distance
from CreateVehicleBS import CreateVehicleBSs, CreateVehicleBSsV2I, CreateVehicleBSsV2V
from Vehicle import Vehicle
from BS import BaseStation
from Network import Network
from scipy.optimize import linprog
from Draw import drawPointPaths

def Run(Num):
    nodes_BS = CreateVehicleBSsV2V(Num)
    vehicles = []
    BSs = []

    # for i in range(3):
    #     BSs[i].cal_num = 15



    for i in range(len(nodes_BS[0])):
        vehicles.append(Vehicle(nodes_BS[0][i][0], nodes_BS[0][i][1]))

    for i in range(len(nodes_BS[1])):
        BSs.append(BaseStation(nodes_BS[1][i][0], nodes_BS[1][i][1]))

    for i in range(len(vehicles)):
        vehicles[i].index = i

    for i in range(len(BSs)):
        BSs[i].index = i

    links = Network(vehicles, BSs)

    # init

    for i in range(-3, 0):
        BSs[i].cal_num = 15
        BSs[i].cal_capacity = random.randint(10, 20)/10

    for vehicle in vehicles:
        vehicle.index = vehicles.index(vehicle)

    for BS in BSs:
        BS.index = BSs.index(BS)

    for BS in BSs:
        for vehicle in vehicles:
            vehicle.layers.append(int(Distance(vehicle.position_x, BS.position_x, vehicle.position_y, BS.position_y)/CommunicationRange))


    for vehicle in vehicles:
        for layer_i in range(len(vehicle.layers)):
            BSs[layer_i].each_layer_vehicles[vehicle.layers[layer_i]].append(vehicle)


    # init


    over_delay = 0
    for vehicle in vehicles:

        over_delay += vehicle.task/vehicle.cal_capacity

        # print(vehicle.valuation, vehicle.task/vehicle.cal_capacity)

    return over_delay/len(vehicles)


if __name__ == '__main__':
    # Run(40)

    RepeatNum = 40

    for i in range(8):
        result = []
        for j in range(RepeatNum):
            result.append(Run(10 + i * 5))
        print(sum(result) / len(result))