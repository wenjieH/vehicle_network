import math
from Parameters import CommunicationRange


# SNR 必要模型参数
SPdistance = 100
length = 800
noise = 10 ** (-93/10 - 3)
Upower = -50
Bandwidth = 5*1e6
P = 0.1
fc = 915*1e6
Ad = 4.11  #antenna gain
de = 3

# Communication_Range = 100

def Shannon(x1, x2, y1, y2):#输入就是坐标
    distance = ((x1-x2)**2+(y1-y2)**2)**(1/2)
    if distance == 0:
        distance = 0.1

    if distance <= CommunicationRange:
        hi = Ad*(3*1e8)**de/(((4*math.pi*fc)**de)*(distance)**(de))
        result = Bandwidth*math.log2(1+P*hi/noise) / 1024/1024/8
    else:
        result = 0.00001

    return result * 10


if __name__ == '__main__':
    for i in range(100):
        print(Shannon(0, 0, 0, i))