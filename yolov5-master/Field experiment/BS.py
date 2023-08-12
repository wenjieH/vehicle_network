import random


class BaseStation():
    def __init__(self, pos_x, pos_y, type:int):
        self.position_x = pos_x
        self.position_y = pos_y

        self.each_layer_vehicles = [[], [], [], [], [], [], [], [], [], []]
        self.para_num = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.off_vehicles = []
        self.cal_num = 15


        self.cal_capacity = 0
        self.cal_num_capacity = 0
        self.index = 0

        if type == 1:
            self.initCal1()
        elif type == 2:
            self.initCal2()

    def initCal1(self):
        self.cal_capacity = random.randint(50, 100) / 3
        self.cal_num_capacity = 20

    def initCal2(self):
        self.cal_capacity = random.randint(10, 20) / 3
        self.cal_num_capacity = 5