import random

from Parameters import CommunicationRange, MaxValue, Max_layer, Distance
from CreateVehicleBS import CreateVehicleBSs, CreateVehicleBSsV2I, CreateVehicleBSsV2VNew, GetVehicleData
from Vehicle import Vehicle
from BS import BaseStation
from Network import Network
import copy

from scipy.optimize import linprog
from Draw import drawPointPaths

def Run(Num):
    nodes_BS = CreateVehicleBSsV2VNew(Num)

    vehicle_data = GetVehicleData(Num)
    OutputVehicle = []
    for a_vehicle in vehicle_data:
        vehicle_use = copy.deepcopy(a_vehicle[0])
        # print(vehicle)
        OutputVehicle.append(
            [vehicle_use['VehicleID'],
             [vehicle_use['LongtitudePosition(meter)'], vehicle_use['LatitudePosition(meter)']],
             vehicle_use['Time(s)'], vehicle_use['Speed(m/s)']])

    print(nodes_BS)

    # nodes_BS = CreateVehicleBSs(Num)
    vehicles = []
    BSs = []

    for i in range(len(nodes_BS[0])):
        # print(nodes_BS[0][i][1][1], nodes_BS[0][i][1][0])
        vehicles.append(Vehicle(nodes_BS[0][i][1][1], nodes_BS[0][i][1][0]))

    for i in range(len(nodes_BS[1])):
        BSs.append(BaseStation(nodes_BS[1][i][0], nodes_BS[1][i][1]))

    for i in range(len(vehicles)):
        vehicles[i].index = i

    for i in range(len(BSs)):
        BSs[i].index = i

    links = Network(vehicles, BSs)

    # init

    # for i in range(-3, 0):
    #     BSs[i].cal_num = 15
    #     BSs[i].cal_capacity = random.randint(10, 20)*500

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

    for vehicle in vehicles:
        for BS in BSs:
            if vehicle in BS.each_layer_vehicles[0]:
                vehicle.offload_decision = BS.index
                BS.off_vehicles.append(vehicle)

    over_delay = 0
    for vehicle in vehicles:

        if vehicle.offload_decision != -1:
            # print(vehicle)
            vehicle_delay = vehicle.task/links.link_v2i[vehicle.index][BSs[vehicle.offload_decision].index] +\
                          len(BSs[vehicle.offload_decision].off_vehicles) * vehicle.task/BSs[vehicle.offload_decision].cal_capacity

            over_delay += vehicle_delay
        else:
            vehicle_delay = vehicle.task/vehicle.cal_capacity

            over_delay += vehicle_delay
            # print(system_profit, vehicle_delay, vehicle.valuation, vehicle.deadline)
    return over_delay/len(vehicles)
    # print(system_profit, vehicle_delay, vehicle.valuation, vehicle.deadline)


if __name__ == '__main__':
    RepeatNum = 40
    print('v2i')
    for i in range(8):
        result = []
        for j in range(RepeatNum):
            result.append(Run(10 + i * 5))
        print(sum(result) / len(result))