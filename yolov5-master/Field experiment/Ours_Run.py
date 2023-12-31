import random

from Parameters import CommunicationRange, MaxValue, Max_layer, Distance
# from CreateVehicleBS import CreateVehicleBSs, CreateVehicleBSsV2VNew, GetVehicleData, GetCandiVehicleData
from Vehicle import Vehicle
from BS import BaseStation
from Network import Network
from scipy.optimize import linprog
from Draw import drawPointPaths
import copy




def CreateVehicleBSsField():
    vehicles = [[0.5, 0.2], [0.5, 0.4], [1, 0.2], [1, 0.3], [1.5, 1.8], [1.5, 1.9], [1.5, 2], [2, 1.6], [2, 1.8]]
    BSs = [[1, 1]]

    return [vehicles, BSs]


def Run(vehicle_coorset, vehicle_num):

    nodes_BS = CreateVehicleBSsField()
    for i in range(len(vehicle_num)):
        nodes_BS[0][vehicle_num[i]] = vehicle_coorset[i]


    print(nodes_BS)
    # nodes_BS = CreateVehicleBSs(Num)
    vehicles = []
    BSs = []


    for i in range(len(nodes_BS[0])):
        # print(nodes_BS[0][i][1][1], nodes_BS[0][i][1][0])
        vehicles.append(Vehicle(nodes_BS[0][i][0] * 100, nodes_BS[0][i][1] * 100))
    # print(len(vehicles))


    for i in range(len(nodes_BS[1])):
        BSs.append(BaseStation(nodes_BS[1][i][0] * 100, nodes_BS[1][i][1] * 100, 1))


    for i in range(len(vehicles)):
        vehicles[i].index = i

    for i in range(len(BSs)):
        BSs[i].index = i


    links = Network(vehicles, BSs)

    # init


    for vehicle in vehicles:
        vehicle.index = vehicles.index(vehicle)

    for BS in BSs:
        BS.index = BSs.index(BS)



    for BS in BSs:
        for vehicle in vehicles:
            vehicle.layers.append(int(Distance(vehicle.position_x, BS.position_x, vehicle.position_y, BS.position_y)/CommunicationRange))

    # 计算每一层得时延
    for vehicle in vehicles:
        all_BS_layer = []
        for layer in vehicle.layers:
            a_BS_layer = []
            for m in range(layer+1):
                a_BS_layer.append(0)
            all_BS_layer.append(a_BS_layer)
        vehicle.layer_transmit = all_BS_layer
        # print('layer_transmit', vehicle.layer_transmit)


    for vehicle in vehicles:
        vehicle.layer_transmit_error = copy.deepcopy(vehicle.layer_transmit)
        vehicle.layers_error = copy.deepcopy(vehicle.layer_transmit)

        vehicle.estimate_layer_delay = copy.deepcopy(vehicle.layer_transmit)
        for BS in BSs:
            vehicle.compute_error.append(0)



    # for vehicle in vehicles:
    #     print(vehicle.layer_transmit)

    for vehicle in vehicles:
        for layer_i in range(len(vehicle.layers)):
            BSs[layer_i].each_layer_vehicles[vehicle.layers[layer_i]].append(vehicle)

    for vehicle in vehicles:
        vehicle.estimate_delay = 0
        vehicle.true_delay = 0
        # print('init', vehicle.estimate_delay, vehicle.true_delay)

    # print(links.get_path_cost([47, 30]))

    # for vehicle in vehicles:
    #     print([vehicle.position_x, vehicle.position_y])

    total_BS_cap = []
    for BS in BSs:
        # print(BS.cal_capacity)
        total_BS_cap.append(BS.cal_capacity)


    count = 1
    while 1:

        for vehicle in vehicles:

            vehicle_estimate = []
            for BS in BSs:
                vehicle_layer = vehicle.layers[BS.index]

                trans_rate = []
                if vehicle_layer == 0:
                    trans_rate.append(links.link_v2i[vehicle.index][BS.index] / BS.para_num[0])
                else:
                    for i in range(vehicle_layer + 1):
                        if i == 0:
                            layer_link = links.GetLayerRate(BS.index, 0)
                        else:
                            layer_link = links.GetLayerRate(BS.index, i)
                        if layer_link == []:
                            layer_link = [10]

                        paral_num = BS.para_num[i]
                        if paral_num >= len(layer_link):
                            trans_rate.append(sum(layer_link) / paral_num)
                        else:
                            # print(paral_num)
                            trans_rate.append(sum(layer_link[:paral_num]) / paral_num)

                # print(trans_rate)
                vehicle.estimate_delay = 0

                for i in range(len(vehicle.layer_transmit[BS.index])):
                    vehicle.layer_transmit[BS.index][i] = vehicle.task / trans_rate[i]

                vehicle.layer_transmit[BS.index] = vehicle.layer_transmit[BS.index][::-1]

                for i in range(len(trans_rate)):
                    if trans_rate[i] == 0:
                        vehicle.estimate_delay += MaxValue
                        vehicle.estimate_layer_delay[BS.index][i] = MaxValue
                    else:
                        vehicle.estimate_delay += vehicle.task / trans_rate[i] + vehicle.layer_transmit_error[BS.index][
                            i]
                        vehicle.estimate_layer_delay[BS.index][i] = vehicle.task / trans_rate[i] + \
                                                                    vehicle.layer_transmit_error[BS.index][i] + \
                                                                    vehicle.layers_error[BS.index][i]

                # add cal
                vehicle_estimate.append(
                    sum(vehicle.estimate_layer_delay[BS.index]) + BS.para_num[1] * vehicle.task / BS.cal_capacity +
                    vehicle.compute_error[BS.index])

            # print('vehicle_estimate', vehicle_estimate)
            vehicle.estimate_delay = min(vehicle_estimate)

            # print('estimate_compare', vehicle.estimate_delay, vehicle.task / vehicle.cal_capacity, vehicle_estimate.index(min(vehicle_estimate)), vehicle.valuation - vehicle.estimate_delay > 0 , vehicle.estimate_delay < vehicle.deadline , vehicle.estimate_delay < vehicle.task/vehicle.cal_capacity)
            if vehicle.valuation - vehicle.estimate_delay > 0 and vehicle.estimate_delay < vehicle.deadline and vehicle.estimate_delay < vehicle.task / vehicle.cal_capacity:
                # BSs[vehicle_estimate.index(min(vehicle_estimate))].off_vehicles.append(vehicle)
                vehicle.offload_decision = vehicle_estimate.index(min(vehicle_estimate))

        # for BS in BSs:
        #     print('off_vehicles:', BS.off_vehicles)

        off_es_num = 0
        off_es_set = []
        for vehicle in vehicles:
            if vehicle.offload_decision != -1:
                off_es_num += 1
                off_es_set.append(vehicle.index)

        for vehicle in vehicles:
            vehicle.offload_decision = -1

        cal_set = []
        for BS in BSs:
            cal_set.append(BS.cal_capacity)
        # print('cal_set:', cal_set)

        # print('off_es_num', off_es_num)


        for m in range(len(BSs)):

            # print(off_es_num,  sum(total_BS_cap[m:]))
            off_es_num_s = int(off_es_num * BSs[m].cal_capacity / sum(total_BS_cap[m:]))
            # print('off_es_num_s', off_es_num_s)
            if off_es_num_s <= BSs[m].cal_num_capacity:
                for i in range(len(off_es_set)):
                    for j in range(i, len(off_es_set)):
                        if vehicles[off_es_set[i]].valuation - sum(
                                vehicles[off_es_set[i]].estimate_layer_delay[BSs[m].index]) < vehicles[
                            off_es_set[j]].valuation - sum(vehicles[off_es_set[j]].estimate_layer_delay[BSs[m].index]):
                            off_es_set[i], off_es_set[j] = off_es_set[j], off_es_set[i]

                for i in range(off_es_num_s):
                    vehicles[off_es_set[i]].offload_decision = m
                    # print(vehicles[off_es_set[i]].offload_decision)
                    # BS.off_vehicles.append(off_es_set[i])

                off_es_set = off_es_set[off_es_num_s:]
                off_es_num -= off_es_num_s
                if off_es_num <= 0:
                    break
            else:

                off_es_num_s = BSs[m].cal_num_capacity
                for i in range(len(off_es_set)):
                    for j in range(i, len(off_es_set)):
                        if vehicles[off_es_set[i]].valuation - sum(
                                vehicles[off_es_set[i]].estimate_layer_delay[BSs[m].index]) < vehicles[
                            off_es_set[j]].valuation - sum(vehicles[off_es_set[j]].estimate_layer_delay[BSs[m].index]):
                            off_es_set[i], off_es_set[j] = off_es_set[j], off_es_set[i]

                # print('off_es_num_s2', off_es_num_s)
                # print('off_es_num_s3', off_es_num_s, len(off_es_set))
                for i in range(off_es_num_s):
                    vehicles[off_es_set[i]].offload_decision = m
                    # print(vehicles[off_es_set[i]].offload_decision)
                    # BS.off_vehicles.append(off_es_set[i])

                off_es_set = off_es_set[off_es_num_s:]
                # print('off_es_num_s4', off_es_num_s, len(off_es_set))
                off_es_num -= off_es_num_s
                if off_es_num <= 0:
                    break

        # for BS in BSs:

        off_set = []
        for vehicle in vehicles:
            off_set.append(vehicle.offload_decision)
        # print('off_set', off_set)

        for vehicle in vehicles:
            if vehicle.offload_decision != -1:
                BSs[vehicle.offload_decision].off_vehicles.append(vehicle)

        # for i in range(len(vehicles)):
        #     if i in [0, 5]:
        #         vehicles[i].offload_decision = 0
        #     elif i in [6, 10]:
        #         vehicles[i].offload_decision = 1

        ##   offload execution
        offload_set = []
        offload_path_set = []
        for vehicle in vehicles:
            if vehicle.offload_decision != -1:

                path = links.find_nodeToBS_route(vehicle.index, vehicle.offload_decision)
                # print('path', path)
                if path == []:
                    # print(BSs[vehicle.offload_decision])
                    BSs[vehicle.offload_decision].off_vehicles.remove(vehicle)
                    vehicle.offload_decision = -1
                    continue
                vehicle.off_path = path
                # print('path', path)

                links.add_path_cost(path)
                offload_set.append(vehicle.index)
                offload_path_set.append(path)

        ##   iterative
        for vehicle in vehicles:
            if vehicle.offload_decision != -1:
                # print('pathcost:', vehicle.task * links.get_path_cost(vehicle.off_path), len(BSs[vehicle.offload_decision].off_vehicles) * vehicle.task/BSs[vehicle.offload_decision].cal_capacity, len(BSs[vehicle.offload_decision].off_vehicles), BSs[vehicle.offload_decision].cal_capacity)
                vehicle.true_delay = vehicle.task * links.get_path_cost(vehicle.off_path) + \
                                     len(BSs[vehicle.offload_decision].off_vehicles) * vehicle.task / BSs[
                                         vehicle.offload_decision].cal_capacity

                # print("delay_Compar", vehicle.estimate_delay, vehicle.true_delay)
                if vehicle.valuation - vehicle.true_delay > 0 and vehicle.true_delay < vehicle.deadline and vehicle.true_delay < vehicle.task / vehicle.cal_capacity:
                    vehicle.off_win = 1
            else:
                vehicle.true_delay = vehicle.task / vehicle.cal_capacity

        for BS in BSs:
            for layer_vehicle in BS.each_layer_vehicles:
                layer_total_num = 0
                layer_win_num = 0
                for vehicle in layer_vehicle:
                    if vehicle.offload_decision != -11:
                        layer_total_num += 1
                    if vehicle.off_win == 1:
                        layer_win_num += 1

                # print(layer_win_num, layer_total_num)
                # print('off_Compar', BS.para_num[BS.each_layer_vehicles.index(layer_vehicle)], layer_win_num, layer_total_num)
                if layer_total_num > 0:
                    if layer_win_num / layer_total_num > 0.7:
                        if BS.para_num[BS.each_layer_vehicles.index(layer_vehicle)] > 1:
                            BS.para_num[BS.each_layer_vehicles.index(layer_vehicle)] -= 1
                    else:
                        if BS.para_num[BS.each_layer_vehicles.index(layer_vehicle)] < layer_total_num:
                            BS.para_num[BS.each_layer_vehicles.index(layer_vehicle)] += 1

        # error calculation
        for vehicle in vehicles:
            if vehicle.offload_decision != -1:
                path_layer = []
                for point in vehicle.off_path[:-1]:
                    path_layer.append(vehicles[point].layers[vehicle.offload_decision])

                arr = path_layer
                arr_b = vehicle.off_path
                result = []
                result_b = []
                result_c = []
                current_subarray = [arr[0]]
                current_subarray_b = [arr_b[0]]
                for i in range(1, len(arr)):
                    if arr[i] == arr[i - 1]:
                        current_subarray.append(arr[i])
                        current_subarray_b.append(arr_b[i])
                    else:
                        result.append(current_subarray)
                        result_b.append(current_subarray_b)
                        current_subarray = [arr[i]]
                        current_subarray_b = [arr_b[i]]

                # Append the last subarray
                result.append(current_subarray)
                result_b.append(current_subarray_b)

                for i in range(len(result_b) - 1):
                    item = []
                    item = result_b[i]
                    item.append(result_b[i + 1][0])
                    result_c.append(item)

                last_result_b = result_b[-1]
                last_result_b.append(vehicle.offload_decision)
                result_c.append(last_result_b)
                # print('path_layer:', path_layer)
                # print(result, result_b)
                #
                # print(vehicle.layer_transmit_error[vehicle.offload_decision], vehicle.off_path)
                for i in range(len(vehicle.layer_transmit_error[vehicle.offload_decision])):
                    if i == len(vehicle.layer_transmit_error[vehicle.offload_decision]) - 1:
                        # print('result get_path_cost', result_c, result_c[i])
                        true_layerdelay = vehicle.task * links.get_path_cost(result_c[i])
                    else:
                        # print('result get_path_cost_no_BS', result_c, result_c[i])
                        true_layerdelay = vehicle.task * links.get_path_cost_no_BS(result_c[i])
                    estimate_layerdelay = vehicle.estimate_layer_delay[vehicle.offload_decision][i]
                    vehicle.layers_error[vehicle.offload_decision][i] = (vehicle.layers_error[vehicle.offload_decision][
                                                                             i] + true_layerdelay - estimate_layerdelay) / 2

                    if len(result_b[i]) > 1:
                        # print(result_b[i])
                        true_transdelay = vehicle.task * links.get_path_cost_no_BS(result_b[i])
                        vehicle.layer_transmit_error[vehicle.offload_decision][i] = true_transdelay

                total_off = 0
                for vehicle in vehicles:
                    if vehicle.offload_decision != -1:
                        total_off += 1

                total_cap = 0
                for BS in BSs:
                    # if (len(BS.off_vehicles) * vehicle.task/BS.cal_capacity - BS.para_num[1] * vehicle.task / BS.cal_capacity)/2 > 0:
                    # total_off += len(BS.off_vehicles)
                    total_cap += BS.cal_capacity

                for BS in BSs:
                    BS.para_num[1] = int(total_off * BS.cal_capacity / total_cap)
                    if BS.para_num[1] == 0:
                        BS.para_num[1] = 1

        all_compute_error = []
        for vehicle in vehicles:
            if vehicle.offload_decision != -1:
                # print(BSs[vehicle.offload_decision].off_vehicles, BSs[vehicle.offload_decision].para_num[1], all_compute_error)
                all_compute_error.append((len(BSs[vehicle.offload_decision].off_vehicles) -
                                          BSs[vehicle.offload_decision].para_num[1]) * vehicle.task / BSs[
                                             vehicle.offload_decision].cal_capacity / 2)

        for vehicle in vehicles:
            for BS in BSs:
                vehicle.compute_error[BS.index] = (vehicle.compute_error[BS.index] + sum(all_compute_error) / len(
                    all_compute_error)) / 2
            # print('compute_error', vehicle.compute_error)

        # update param
        # if count % 20 == 0:
        #     for BS in BSs:
        #         BS.para_num = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        #
        #         for vehicle in vehicles:
        #             if vehicle.offload_decision != -1:
        #                 BS.para_num[int(Distance(vehicle.position_x, BS.position_x, vehicle.position_y,
        #                              BS.position_y) / CommunicationRange)] += 1
        #
        #         for i in range(len(BS.para_num)):
        #             if BS.para_num[i] > 1:
        #                 BS.para_num[i] -= 1
        #
        #     print('adapt')
        #     for BS in BSs:
        #         print(BS.para_num)
        #
        # off_num = 0
        # for vehicle in vehicles:
        #     if vehicle.offload_decision != -1:
        #         off_num += 1
        # print('off_num:', off_num)

        # for BS in BSs:
        #     print(BS.para_num)

        if count > 10:
            # #   look results

            for vehicle in vehicles:
                if vehicle.off_path == []:
                    vehicle.offload_decision = -1

            paths_element = []
            for vehicle in vehicles:

                if vehicle.offload_decision != -1:
                    paths_element.append(vehicle.off_path[:-1])

            for vehicle in vehicles:

                relay_task = []
                relay_task_valuation = []
                for item_path in paths_element:
                    if vehicle.index in item_path:
                        relay_task.append(item_path)
                        relay_task_valuation.append(vehicles[item_path[0]].valuation)

                # print('relay_task_valuation:', relay_task, relay_task_valuation)
                if len(relay_task) > vehicle.relay_tasknum_capacity:
                    for i in range(len(relay_task)):
                        for j in range(i, len(relay_task)):
                            if relay_task_valuation[i] < relay_task_valuation[j]:
                                relay_task[i], relay_task[j] = relay_task[j], relay_task[i]

                    for item_path in relay_task[vehicle.relay_tasknum_capacity:]:
                        vehicles[item_path[0]].offload_decision = -1

            for BS in BSs:
                if len(BS.off_vehicles) > BS.cal_num_capacity:
                    for i in range(len(BS.off_vehicles)):
                        for j in range(i, len(BS.off_vehicles)):
                            if BS.off_vehicles[i].valuation < BS.off_vehicles[j].valuation:
                                BS.off_vehicles[i], BS.off_vehicles[j] = BS.off_vehicles[j], BS.off_vehicles[i]

                    # print('BS.off_vehicles[BS.cal_num_capacity:]', len(BS.off_vehicles[BS.cal_num_capacity:]))
                    for vehicle in BS.off_vehicles[BS.cal_num_capacity:]:
                        vehicle.offload_decision = -1

            total_valuation = 0
            for vehicle in vehicles:
                if vehicle.offload_decision != -1:
                    if vehicle.task * links.get_path_cost(vehicle.off_path) - \
                            len(BSs[vehicle.offload_decision].off_vehicles) * vehicle.task / BSs[
                        vehicle.offload_decision].cal_capacity < vehicle.deadline:
                        total_valuation += vehicle.valuation - vehicle.task * links.get_path_cost(vehicle.off_path) - \
                                           len(BSs[vehicle.offload_decision].off_vehicles) * vehicle.task / BSs[
                                               vehicle.offload_decision].cal_capacity
                    else:
                        total_valuation += 0
                else:
                    if vehicle.task / vehicle.cal_capacity <= vehicle.deadline:
                        total_valuation += vehicle.valuation - vehicle.task / vehicle.cal_capacity
                    else:
                        total_valuation += 0

            print('total_valuation:', total_valuation)


            sch_results = []
            for vehicle in vehicles:
                sch_results.append([vehicle.off_path, vehicle.offload_decision])

            return sch_results
            # break

        count += 1
        max_system_profit = 0
        for vehicle in vehicles:
            # print('test', vehicle.valuation - vehicle.task/vehicle.cal_capacity)
            if vehicle.task / vehicle.cal_capacity < vehicle.deadline and vehicle.valuation - vehicle.task / vehicle.cal_capacity > 0:
                max_system_profit += vehicle.valuation - vehicle.task / vehicle.cal_capacity

        # print(max_system_profit)
        overall_delay = 0
        for vehicle in vehicles:
            if vehicle.offload_decision != -1:
                overall_delay += vehicle.true_delay
                # print('compare:', vehicle.true_delay, vehicle.task / vehicle.cal_capacity)
            else:
                overall_delay += vehicle.task / vehicle.cal_capacity
        # print('overall_delay:', overall_delay)

        #  clear algorithm loop
        links.clear_load()
        for BS in BSs:
            BS.off_vehicles = []

        for vehicle in vehicles:
            vehicle.error_value = (vehicle.true_delay - vehicle.estimate_delay) / 2
            # print('error', vehicle.error_value)

        for vehicle in vehicles:
            vehicle.offload_decision = -1
            vehicle.off_win = 0
            vehicle.off_path = []
            vehicle.true_delay = 0














if __name__ == '__main__':

    print(Run([[0.5, 0.2]], [0]))
    # RepeatNum = 40
    #
    # for i in range(8):
    #     result = []
    #     for j in range(RepeatNum):
    #         result.append(Run(10+i*5))
    #     print(sum(result)/len(result))
