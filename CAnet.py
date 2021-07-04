# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

net_table = {}
net_table[1] = [4, 28, 26]
net_table[2] = []
net_table[3] = [2, 26, 28]
net_table[4] = []
net_table[5] = [28, 30, 44]
net_table[6] = []
net_table[7] = [30, 10, 32]
net_table[8] = []
net_table[9] = [8, 30, 32]
net_table[10] = []
net_table[11] = [46, 32, 34]
net_table[12] = []
net_table[13] = [34, 16, 36]
net_table[14] = []
net_table[15] = [14, 36, 34]
net_table[16] = []
net_table[17] = [38, 48, 36]
net_table[18] = []
net_table[19] = [22, 40, 38]
net_table[20] = []
net_table[21] = [20, 40, 38]
net_table[22] = []
net_table[23] = [26, 42, 40]
net_table[24] = []
net_table[25] = [24, 40, 42]
net_table[26] = [2, 4, 28]
net_table[27] = [2, 4, 26]
net_table[28] = [6, 30, 44]
net_table[29] = [28, 6, 44]
net_table[30] = [8, 10, 32]
net_table[31] = [30, 8, 10]
net_table[32] = [46, 34, 12]
net_table[33] = [46, 32, 12]
net_table[34] = [36, 16, 14]
net_table[35] = [34, 14, 16]
net_table[36] = [18, 38, 48]
net_table[37] = [18, 36, 48]
net_table[38] = [20, 40, 22]
net_table[39] = [22, 20, 38]
net_table[40] = [24, 26, 42]
net_table[41] = [24, 40, 26]
net_table[42] = [44, 46, 48]
net_table[43] = [28, 6, 30]
net_table[44] = [22, 48, 46]
net_table[45] = [32, 12, 34]
net_table[46] = [42, 44, 48]
net_table[47] = [38, 18, 36]
net_table[48] = [42, 44, 46]

net_table['inlet'] = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]


def RunCA_Net(path=700, n=200, v0=20, ltv=50, p_left_and_right=0.5, p_wander=0, p_slow_down=0.3, rou=0,
              times=300, p_huan=0.2, num_roads=24, vmin_driver=0):
    # 可以假设随机慢速均匀分布   p_slow_down叫做随机慢速
    '''
    path = 700.0 # 道路长度 实际对应路段4.9km
    n = 200 # 车辆数目
    v0 = 20 # 初始速度
    ltv = 50  # 最大限速
    p = 0.3 # 减速概率
    rou = 0 # 自动车的比例
    times = 3000 # 模拟的时间数目 实际单个时间为25.2s
    num_roads=48 #路网中的路段数目

    '''

    '''
    road_index #表明这个车目前行驶在哪个路段上
    x #这个车的局部x坐标
    y #这个车的局部y坐标
    v #这个车的局部速度
    '''

    # x保存每辆车在道路上的x轴位置坐标
    x = np.random.randint(0, path, n)
    x.sort()
    # 每辆车在道路上的y轴位置坐标随机给出
    y = np.random.binomial(1, p_left_and_right, size=n)
    # 让所有车随机分布在所有的路段上
    road_index = np.random.randint(1, 49, n)
    # 保存道路快照 这里要加上路段的数目
    car_distribution = np.zeros((48, path, 2))

    car_distribution[road_index - 1, x, y] = 1

    # 添加自动车的下标数组
    auto_list = np.random.randint(0, n, int(n * rou))
    # v保存每辆车的速度，初速度相同
    v = np.ones((n,), dtype=int) * v0

    # v_mean = np.zeros_like(v)

    q_num = 0

    # 运行公路一段时间
    for t in range(times):

        # 模拟每辆车的行为，包括自动车与普通车

        for i in range(n):

            # x.sort()

            auto_flag = (auto_list == i).any()  # 为真是自动车

            # if x[(i + 1) % n] > x[i]:
            #     d = x[(i + 1) % n] - x[i]
            # else:
            #     d = path - x[i] + x[(i + 1) % n]

            # #首先进行特例的判断
            # if x[i]+d>path-1:

            # 像人的视线一样计算当前车与前车的距离以及和另一个车道上前车的距离，如果另一个车道上前车距离更大那么有一定几率换道

            d1 = 1  # 当前道路

            d2 = 1  # 另一个道路

            while car_distribution[road_index[i] - 1, (x[i] + d1) % path, y[i]] == 0 and d1 <= ltv:
                d1 = d1 + 1

            while car_distribution[road_index[i] - 1, (x[i] + d2) % path, 1 - y[i]] == 0 and d2 <= ltv:
                d2 = d2 + 1

            if d2 > d1:

                # 有一定几率按换道规则进行换道

                if np.random.rand() < p_huan:

                    y[i] = 1 - y[i]

                    d = d2

                else:

                    d = d1

            else:

                d = d1

            # 根据距离计算下一秒的速度

            # 自动车的行为是不会随机慢速
            temp_p_slow_down = p_slow_down

            if auto_flag:
                temp_p_slow_down = 0
            if v[i] < d:
                if np.random.rand() > temp_p_slow_down:

                    v[i] += 1
                else:
                    v[i] -= 1
            else:

                v[i] = d - 1

        # 对速度进行限制
        v = v.clip(vmin_driver, ltv)

        # 有一半几率会遇到红灯，在这里考虑 如果遇到红灯，首先将速度降为0,然后x=path-1
        for i in range(v.shape[0]):

            if x[i] + v[i] > path and np.random.rand() > 0.5:

                v[i] = 0

                x[i] = path - 1




        # 一秒后，车辆的位置发生了变化

        x += v

        # q_num是每个时间出车的数目，即流量

        q_sum_array = np.where(x > path, 1, 0)

        q_num += np.sum(q_sum_array)
        # 当前改路车的序号
        change_road_ind = np.argwhere(x > path)
        # 当前改路车的所在路段
        change_road = road_index[change_road_ind]

        change_road = change_road.reshape((change_road.shape[0],))
        change_road = change_road.tolist()

        # 对于每个要改道的车
        for i in range(len(change_road)):

            # s=
            # print(change_road.shape)
            if not net_table[change_road[i]]:

                tmp_dice = np.random.randint(1, len(net_table['inlet']))  # np里面是前闭后开，random里面是前后都闭

                road_index[change_road_ind[i]] = net_table['inlet'][tmp_dice]


            else:

                tmp_dice = np.random.randint(1, len(net_table[change_road[i]]))

                road_index[change_road_ind[i]] = tmp_dice

        x = x % path

        # 更新快照
        car_distribution = np.zeros((48, path, 2))

        car_distribution[road_index - 1, x, y] = 1

    q_num /= times

    return q_num
