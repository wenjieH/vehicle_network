import random


class Vehicle():
    def __init__(self, pos_x, pos_y):
        self.position_x = pos_x
        self.position_y = pos_y
        self.cal_capacity = 0
        self.s_pow = 0
        self.task = 0
        self.index = 0
        self.estimate_delay = 0
        self.true_delay = 0

        self.error_value = 0

        self.layer_transmit = []
        self.layer_transmit_error = []
        self.layers_error = []
        self.estimate_layer_delay = []

        self.compute_error = []

        self.off_win = 0
        self.off_path = []
        self.layers = []
        self.valuation = 0
        self.offload_decision = -1
        self.initTask()



    def initTask(self):
        self.task = random.randint(100, 500)
        self.valuation = random.randint(1500, 1800)
        self.deadline = random.randint(1000, 1500)
        self.cal_capacity = random.uniform(1, 2)/3