from Parameters import CommunicationRange
import math
import random
import numpy as np
from Draw import drawPoints
import copy


# 100*100
def CreateVehicleBSs(num: int):
    BSs = [[150, 500], [450, 500], [750, 500]]
    frame_dis = int(CommunicationRange * 0.9)

    frame_nodes = [[0, -frame_dis], [-frame_dis*math.sin(np.deg2rad(10)), -frame_dis - frame_dis*math.cos(np.deg2rad(10))], [frame_dis*math.sin(np.deg2rad(10)), -frame_dis -frame_dis*math.cos(np.deg2rad(10))]]
    nodes = []
    # for i in range(num):


    for j in range(len(BSs)):

        add_nodes_num = int(num / len(BSs)) - len(frame_nodes)

        double_nodes = []
        for ele in frame_nodes:
            nodes.append([BSs[j][0]+ele[0], BSs[j][1]+ele[1]])
            if frame_nodes.index(ele) > 0:
                double_nodes.append([BSs[j][0]+ele[0], BSs[j][1]+ele[1]])

        # double_nodes = [nodes[-1], nodes[-2]]
        while add_nodes_num > 0:
            choose = random.choice(double_nodes)
            angle = random.randint(-180, 180)
            nodes.append([choose[0]+frame_dis*math.cos(np.deg2rad(angle)), choose[1]+frame_dis*math.sin(np.deg2rad(angle))])
            add_nodes_num -= 1

    for i in range(3):
        BSs.append(random.choice(nodes))

    # print(nodes)
    # drawPoints(BSs, nodes)
    return nodes, BSs


def CreateVehicleBSsV2I(num: int):
    BSs = [[150, 500], [450, 500], [750, 500]]
    frame_dis = int(CommunicationRange * 0.9)

    frame_nodes = [[0, -frame_dis], [-frame_dis*math.sin(np.deg2rad(10)), -frame_dis - frame_dis*math.cos(np.deg2rad(10))], [frame_dis*math.sin(np.deg2rad(10)), -frame_dis -frame_dis*math.cos(np.deg2rad(10))]]
    nodes = []
    # for i in range(num):


    for j in range(len(BSs)):

        add_nodes_num = int(num / len(BSs)) - len(frame_nodes)

        double_nodes = []
        for ele in frame_nodes:
            nodes.append([BSs[j][0]+ele[0], BSs[j][1]+ele[1]])
            if frame_nodes.index(ele) > 0:
                double_nodes.append([BSs[j][0]+ele[0], BSs[j][1]+ele[1]])

        # double_nodes = [nodes[-1], nodes[-2]]
        while add_nodes_num > 0:
            choose = random.choice(double_nodes)
            angle = random.randint(-180, 180)
            nodes.append([choose[0]+frame_dis*math.cos(np.deg2rad(angle)), choose[1]+frame_dis*math.sin(np.deg2rad(angle))])
            add_nodes_num -= 1

    # for i in range(3):
    #     BSs.append(random.choice(nodes))

    # print(nodes)
    # drawPoints(BSs, nodes)
    return nodes, BSs


def CreateVehicleBSsV2V(num: int):
    BSs = [[150, 500], [450, 500], [750, 500]]
    frame_dis = int(CommunicationRange * 0.9)

    frame_nodes = [[0, -frame_dis], [-frame_dis*math.sin(np.deg2rad(10)), -frame_dis - frame_dis*math.cos(np.deg2rad(10))], [frame_dis*math.sin(np.deg2rad(10)), -frame_dis -frame_dis*math.cos(np.deg2rad(10))]]
    nodes = []
    # for i in range(num):


    for j in range(len(BSs)):

        add_nodes_num = int(num / len(BSs)) - len(frame_nodes)

        double_nodes = []
        for ele in frame_nodes:
            nodes.append([BSs[j][0]+ele[0], BSs[j][1]+ele[1]])
            if frame_nodes.index(ele) > 0:
                double_nodes.append([BSs[j][0]+ele[0], BSs[j][1]+ele[1]])

        # double_nodes = [nodes[-1], nodes[-2]]
        while add_nodes_num > 0:
            choose = random.choice(double_nodes)
            angle = random.randint(-180, 180)
            nodes.append([choose[0]+frame_dis*math.cos(np.deg2rad(angle)), choose[1]+frame_dis*math.sin(np.deg2rad(angle))])
            add_nodes_num -= 1

    BSs = []
    for i in range(3):
        BSs.append(random.choice(nodes))
    # print(BSs)

    # print(nodes)
    # drawPoints(BSs, nodes)
    return nodes, BSs

import matplotlib.pyplot as plt
from Importdatabase import mysql

def GetVehicleData(num):
    mysql_test = mysql()
    vehicle_data = mysql_test.FindAllVehicle()

    print(len(vehicle_data))
    vehicle_set = []
    for i in range(num-1):
        vehicle_set.append([])

    for vehicle in vehicle_data:
        if vehicle['VehicleID'] < num:
            # print(vehicle['VehicleID'])
            vehicle_set[vehicle['VehicleID']-1].append(vehicle)




    # uniform distribution
    for i in range(num-1):
        temp = copy.deepcopy(vehicle_set[i][int(i/num * len(vehicle_set[i])):])
        temp.extend(vehicle_set[i][:int(i/num * len(vehicle_set[i]))])
        vehicle_set[i] = temp

    return vehicle_set

def GetCandiVehicleData(num):
    mysql_test = mysql()
    vehicle_data = mysql_test.FindAllVehicle()

    # print(len(vehicle_data))
    vehicle_set = []
    for i in range(num-1):
        vehicle_set.append([])

    # print(len(vehicle_set))

    for vehicle in vehicle_data:
        if vehicle['VehicleID'] >= 200 and vehicle['VehicleID'] < num + 200-1:
            # print(vehicle['VehicleID'])
            vehicle_set[vehicle['VehicleID']-200].append(vehicle)

    # uniform distribution
    for i in range(num-1):
        temp = copy.deepcopy(vehicle_set[i][int(i/num * len(vehicle_set[i])):])
        temp.extend(vehicle_set[i][:int(i/num * len(vehicle_set[i]))])
        vehicle_set[i] = temp

    OutputCandiVehicle = []
    for a_vehicle in vehicle_set:
        # print(len(a_vehicle))
        vehicle = copy.deepcopy(a_vehicle[0])
        # print(vehicle)
        OutputCandiVehicle.append([vehicle['VehicleID'], [vehicle['LongtitudePosition(meter)'], vehicle['LatitudePosition(meter)']],
             vehicle['Time(s)'], vehicle['Speed(m/s)']])

    return OutputCandiVehicle



def CreateVehicleBSsV2VNew(num):
    vehicle_set = GetVehicleData(num)
    # print(vehicle_set[0])
    OutputVehicle = []
    for a_vehicle in vehicle_set:
        # print(len(a_vehicle))
        vehicle = copy.deepcopy(a_vehicle[0])
        # print(vehicle)
        OutputVehicle.append([vehicle['VehicleID'], [vehicle['LatitudePosition(meter)'], vehicle['LongtitudePosition(meter)']], vehicle['Time(s)'], vehicle['Speed(m/s)']])

    # candidate_set = GetVehicleData(20)
    # for a_vehicle in vehicle_set:
    #     candi_vehicle = copy.deepcopy(a_vehicle[0])

    # print(OutputVehicle)
    BSs = [[0, 0], [0, 400], [4, 200]]
    return [OutputVehicle, BSs]


def CreateVehicleBSsField():
    vehicles = [[0.45, 0.2], [0.45, 0.4], [0.9, 0.1], [0.9, 0.2], [0.9, 0.3], [1.35, 1.8], [1.35, 1.9], [1.35, 2], [1.8, 1.6], [1.8, 1.8]]
    BSs = [[0, 1], [2, 1]]

    return [vehicles, BSs]


if __name__ == '__main__':
    CreateVehicleBSsV2VNew(100)
    print(GetCandiVehicleData(20))