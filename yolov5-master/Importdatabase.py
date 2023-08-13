# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import math
import random
import copy
import pymysql
import matplotlib.pyplot as plt
# kobeavril0928
class mysql(object):
    def __init__(self):
        self.config = {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': 'kobeavril0928', 'db': 'vehiclenetwork',  'charset': 'utf8mb4'}
        self.db = pymysql.connect(**self.config, cursorclass = pymysql.cursors.DictCursor)
        self.cursor = self.db.cursor()

    def connect(self):
        self.db = pymysql.connect(**self.config, cursorclass = pymysql.cursors.DictCursor)
        self.cursor = self.db.cursor()


    def FindAllVehicle(self):
        self.connect()
        sql = "SELECT * FROM vehicles"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.db.close()
            return result
        except Exception as e:
            print(e)
            self.db.rollback()
            self.db.close()
            return

    def FindAllFieldData(self):
        self.connect()
        sql = "SELECT * FROM fielddata"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.db.close()
            return result
        except Exception as e:
            print(e)
            self.db.rollback()
            self.db.close()
            return

    def FindAllFuzzy(self):
        self.connect()
        sql = "SELECT * FROM fuzzy"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.db.close()
            return result
        except Exception as e:
            print(e)
            self.db.rollback()
            self.db.close()
            return

    def UpdateVehicle(self, lat: float, lng: float, num: int):
        self.connect()
        print(lat, lng, num)
        sql = "UPDATE fielddata SET lat = '%s', lng = '%s' WHERE num = '%s'"% (lat, lng, num)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.db.close()
            # print('save durantion success')
            return 1
        except Exception as e:
            print(e)
            self.db.rollback()
            self.db.close()
            return 0

    def Insertfuzzy(self, dis, ddl, den, rat, pro):
        self.connect()
        sql = "INSERT INTO fuzzy(dis, ddl, den, rat, pro) VALUES(%s, %s, %s, %s, %s)" % (dis, ddl, den, rat, pro)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.db.close()
            # print('save durantion success')
            return 1
        except Exception as e:
            print(e)
            self.db.rollback()
            self.db.close()
            return 0




def OutputFromLoc():
    mysql_test = mysql()
    order_data = mysql_test.FindAllOrder()
    lat_lngs = []
    list_x = []
    list_y = []

    for order in order_data:
        if int(order['FromLat']) == 0 and int(order['FromLng']) == 0:
            continue
        lat_lngs.append([order['FromLat'], order['FromLng']])
        list_x.append(order['FromLat'])
        list_y.append(order['FromLng'])
    return lat_lngs


def OutputToloc():
    mysql_test = mysql()
    order_data = mysql_test.FindAllOrder()
    lat_lngs = []
    list_x = []
    list_y = []

    for order in order_data:
        if int(order['ToLat']) == 0 and int(order['ToLng']) == 0:
            continue
        lat_lngs.append([order['ToLat'], order['ToLng']])
        list_x.append(order['ToLat'])
        list_y.append(order['ToLng'])
    return lat_lngs


# from Plot import plot_gps_points
# import matplotlib.pyplot as plt

def plot_single_trajectory(trajectory, color):
    x_vals = [point[0] for point in trajectory]
    y_vals = [point[1] for point in trajectory]
    plt.plot(x_vals, y_vals, color=color)



if __name__ == '__main__':
    mysql_test = mysql()
    vehicle_data = mysql_test.FindAllVehicle()
    mysql_test.UpdateVehicle(0.6, 0.2, 1)