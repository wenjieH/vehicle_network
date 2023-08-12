from typing import List
from Vehicle import Vehicle
from BS import BaseStation
from Shannon import Shannon
from copy import deepcopy
# from
from Parameters import Max_layer
# from CreateVehicleBS import CreateVehicleBSs, CreateVehicleBSsV2VNew, GetVehicleData, GetCandiVehicleData
import copy

class Network():
    def __init__(self, Vehicles: List[Vehicle], BSs: List[BaseStation]):
        self.vehicles = Vehicles
        self.BSs = BSs
        self.link_v2v = []
        self.link_load_v2v =[]
        self.link_v2i = []
        self.link_load_v2i = []
        self.initLink()

    def initLink(self):
        for vehicle1 in self.vehicles:
            vehicle_vehicle_link = []
            vehicle_vehicle_load = []
            for vehicle2 in self.vehicles:
                vehicle_vehicle_link.append(Shannon(vehicle1.position_x, vehicle2.position_x, vehicle1.position_y, vehicle2.position_y))
                vehicle_vehicle_load.append(1)
            self.link_v2v.append(vehicle_vehicle_link)
            self.link_load_v2v.append(vehicle_vehicle_load)

        for vehicle in self.vehicles:
            BS_vechile_link = []
            BS_vechile_load = []
            for BS in self.BSs:
                BS_vechile_link.append(Shannon(vehicle.position_x, BS.position_x, vehicle.position_y, BS.position_y))
                BS_vechile_load.append(1)
            self.link_v2i.append(BS_vechile_link)
            self.link_load_v2i.append(BS_vechile_load)

    def GetLayerRate(self, BS_index, layer):
        if layer == 0:
            vehicle_set0 = self.BSs[BS_index].each_layer_vehicles[0]
            link_rate_set = []
            for vehicle0 in vehicle_set0:
                # print(vehicle0, self.link_v2i)
                link_rate_set.append(self.link_v2i[vehicle0.index][BS_index])
            return link_rate_set

        vehicle_set1 = self.BSs[BS_index].each_layer_vehicles[layer]
        vehicle_set2 = self.BSs[BS_index].each_layer_vehicles[layer - 1]
        link_rate_set = []
        for vehicle1 in vehicle_set1:
            for vehicle2 in vehicle_set2:
                link_rate_set.append(self.link_v2v[vehicle1.index][vehicle2.index])

        link_rate_set.sort(reverse=True)
        while 1e-05 in link_rate_set:
            link_rate_set.remove(1e-05)

        newlink_rate_set=[]
        for link in link_rate_set:
            if link > 3:
                newlink_rate_set.append(link)

        return newlink_rate_set


    def dijkstra(self, matrix, source):
        M = 1E100
        n = len(matrix)
        m = len(matrix[0])
        if source >= n or n != m:
            print('Error!')
            return
        found = [source]  # 已找到最短路径的节点
        cost = [M] * n  # source到已找到最短路径的节点的最短距离
        cost[source] = 0
        path = [[]] * n  # source到其他节点的最短路径
        path[source] = [source]
        while len(found) < n:  # 当已找到最短路径的节点小于n时
            min_value = M + 1
            col = -1
            row = -1
            for f in found:  # 以已找到最短路径的节点所在行为搜索对象
                for i in [x for x in range(n) if x not in found]:  # 只搜索没找出最短路径的列
                    if matrix[f][i] + cost[f] < min_value:  # 找出最小值
                        min_value = matrix[f][i] + cost[f]  # 在某行找到最小值要加上source到该行的最短路径
                        row = f  # 记录所在行列
                        col = i
            if col == -1 or row == -1:  # 若没找出最小值且节点还未找完，说明图中存在不连通的节点
                break
            found.append(col)  # 在found中添加已找到的节点
            cost[col] = min_value  # source到该节点的最短距离即为min_value
            path[col] = path[row][:]  # 复制source到已找到节点的上一节点的路径
            path[col].append(col)  # 再其后添加已找到节点即为sorcer到该节点的最短路径
        return found, cost, path

    def generate_matrix(self, BS_index):
        M = 1E100
        matrix = deepcopy(self.link_v2v)


        # 添加一行
        row = []
        for i in range(len(self.vehicles)):
            row.append(self.link_v2i[i][BS_index])

        # 添加一列
        matrix.append(row)
        for i in range(len(matrix[:-1])):
            matrix[i].append(int(self.link_v2i[i][BS_index]))

        matrix[-1].append(0)
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] >= 0.01:
                    if i < len(self.vehicles) and j < len(self.vehicles):
                        matrix[i][j] = round(self.link_load_v2v[i][j] / self.link_v2v[i][j], 3)
                    else:
                        if j == len(self.vehicles) and i < len(self.vehicles):
                            matrix[i][j] = round(
                                self.link_load_v2i[i][BS_index] / self.link_v2i[i][BS_index], 3)
                        elif i == len(self.vehicles) and j < len(self.vehicles):
                            matrix[i][j] = round(
                                self.link_load_v2i[j][BS_index] / self.link_v2i[j][BS_index], 3)

                else:
                    matrix[i][j] = M

        return matrix

    def find_nodeToBS_route(self, node_index, BS_index):

        matrix = self.generate_matrix(BS_index)

        # print(self.dijkstra(matrix, node_index))
        found, cost, paths = self.dijkstra(matrix, node_index)

        path_result = []
        cost_result = float("inf")

        if len(paths[-1]) > 1:
            path_result = paths[-1]
            cost_result = cost[-1]
            path_result[-1] = BS_index

        return path_result

    def find_end_route(self, node_index):
        paths = []
        cost_paths = []
        for BS in self.BSs:
            path, cost_path = self.find_nodeToBS_route(node_index, BS.index)
            paths.append(path)
            cost_paths.append(cost_path)

        end_path = paths[cost_paths.index(min(cost_paths))]  # 最终节点选择的基站
        return end_path, min(cost_paths)


    def add_path_cost(self, path):
        for i in range(len(path))[:-2]:
            self.link_load_v2v[path[i]][path[i+1]] += 1
        # print(path)
        self.link_load_v2i[path[-2]][path[-1]] += 1

    def get_path_cost(self, path):
        cost = 0
        for i in range(len(path))[:-2]:
            cost += self.link_load_v2v[path[i]][path[i+1]] / self.link_v2v[path[i]][path[i+1]]
        cost += self.link_load_v2i[path[-2]][path[-1]] / self.link_v2i[path[-2]][path[-1]]
        return cost

    def get_path_cost_no_BS(self, path):
        cost = 0
        for i in range(len(path))[:-1]:
            cost += self.link_load_v2v[path[i]][path[i+1]] / self.link_v2v[path[i]][path[i+1]]
        # cost += self.link_load_v2i[path[-2]][path[-1]] / self.link_v2i[path[-2]][path[-1]]
        return cost

    def clear_load(self):
        for i in range(len(self.link_load_v2i)):
            for j in range(len(self.link_load_v2i[0])):
                self.link_load_v2i[i][j] = 1

        for i in range(len(self.link_load_v2v)):
            for j in range(len(self.link_load_v2v[0])):
                self.link_load_v2v[i][j] = 1









if __name__ == '__main__':

    Num = 100
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
        vehicles.append(Vehicle(nodes_BS[0][i][1][0], nodes_BS[0][i][1][1]))
    # print(len(vehicles))

    candidate_vehicle = GetCandiVehicleData(20)

    for i in range(len(nodes_BS[1])):
        BSs.append(BaseStation(nodes_BS[1][i][0], nodes_BS[1][i][1], 1))

    for candi_vehicle in candidate_vehicle:
        BSs.append(BaseStation(candi_vehicle[1][0], candi_vehicle[1][1], 2))

    for i in range(len(vehicles)):
        vehicles[i].index = i

    for i in range(len(BSs)):
        BSs[i].index = i

    links = Network(vehicles, BSs)
    m = 6
    print(vehicles[m].position_x,  vehicles[m].position_y)
    n = 2
    print(BSs[n].position_x, BSs[n].position_y)
    print(links.find_nodeToBS_route(m, n))