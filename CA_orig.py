# -*- coding: utf-8 -*-

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


matplotlib.rcParams['axes.unicode_minus'] = False
np.random.seed(0)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False



vmin_law = 0

vmin_driver = int(vmin_law*1.05)





def Run1d(path=5000, n=100, v0=60, ltv=120, p_slow_down=0.3, p_wander=0,rou=0, times=3000):
    # 可以假设随机慢速均匀分布   p_slow_down叫做随机慢速
    '''
    path = 5000.0 # 道路长度
    n = 100 # 车辆数目
    v0 = 60 # 初始速度
    ltv = 120 # 最大限速
    p = 0.3 # 减速概率
    rou = 0 # 自动车的比例
    times = 3000 # 模拟的时刻数目
    '''

    # x保存每辆车在道路上的位置，随机初始化
    x = np.random.rand(n) * path
    x.sort()
    # v保存每辆车的速度，初速度相同
    v = np.ones(n) * v0

    plt.figure(figsize=(5, 4), facecolor='w')
    # 模拟每个时刻
    for t in range(times):
        plt.scatter(x, [t] * n, s=1, c='k', alpha=0.05)
        # 模拟每辆车
        for i in range(n):
            # 计算当前车与前车的距离
            if x[(i + 1) % n] > x[i]:
                d = x[(i + 1) % n] - x[i]
            else:
                d = path - x[i] + x[(i + 1) % n]
            # 根据距离计算下一秒的速度

            if v[i] < d:
                if np.random.rand() > p_slow_down:
                    v[i] += 1
                else:
                    v[i] -= 1
            else:
                v[i] = d - 1

            


        # 对速度进行限制
        v = v.clip(vmin_driver, ltv)

        

        # if np.random.rand() < p_wander:
        #     v[i]-=1

        # 一秒后，车辆的位置发生了变化
        x += v
        # 注意,周期型边界条件
        x = x % path

    # 展示
    plt.xlim(0, path)
    plt.ylim(0, times)
    plt.xlabel(u'车辆位置')
    plt.ylabel(u'模拟时间')
    plt.title(u'交通模拟(车道长度%d,车辆数%d,初速度%s,减速概率%s)' % (path, n, v0, p_slow_down))

    plt.show()


if __name__ == '__main__':

    Run1d(p_slow_down=0.5)
