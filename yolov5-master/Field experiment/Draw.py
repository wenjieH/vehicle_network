import matplotlib.pyplot as plt

# 绘图查看分布图


def return_distance(x1, x2, y1, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)


def drawPoints(BSs, nodes):
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for BS in BSs:
        x1.append(BS[0])
        y1.append(BS[1])

    for node in nodes:
        x2.append(node[0])
        y2.append(node[1])

    communication_range = 50

    colors = []
    for node in nodes:
        distance = 900
        for BS in BSs:
            if return_distance(node[0], BS[0], node[1], BS[1]) < distance:
                distance = return_distance(node[0], BS[0], node[1], BS[1])

        colors.append(int(distance/communication_range)+1)

    plt.scatter(x1, y1, c='black', marker='^', s=100)
    plt.scatter(x2, y2, c='red', marker='s', s=40)
    plt.colorbar()   # 显示颜色条
    plt.show()


def drawPointPaths(BSs, nodes, nodes_path):
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for BS in BSs:
        x1.append(BS[0])
        y1.append(BS[1])

    for node in nodes:
        x2.append(node[0])
        y2.append(node[1])

    communication_range = 50

    colors = []
    for node in nodes:
        distance = 900
        for BS in BSs:
            if return_distance(node[0], BS[0], node[1], BS[1]) < distance:
                distance = return_distance(node[0], BS[0], node[1], BS[1])

        colors.append(int(distance/communication_range)+1)

    plt.scatter(x1, y1, c='black', marker='^', s=250, alpha=1, cmap='inferno')
    plt.scatter(x2, y2, c=colors, alpha=1, cmap='winter')
    plt.colorbar()   # 显示颜色条


    for path in nodes_path:
        path_x1 = []
        path_y1 = []
        for node_index in path[:-1]:
            path_x1.append(x2[node_index])
            path_y1.append(y2[node_index])

        path_x1.append(x1[path[-1]])
        path_y1.append(y1[path[-1]])

        plt.plot(path_x1, path_y1, color='blue', linestyle='--')

    plt.show()

if __name__ == '__main__':
    pass