# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


matplotlib.rcParams['axes.unicode_minus'] = False
# np.random.seed(0)  有这一行，程序每次生成相同的随机数
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False



vmin_law = 60

vmin_driver = vmin_law+1



def Run1d(path=5000, n=100, v0=80, ltv=120, p_wander=0, p_slow_down=0.3,rou=0, times=3000):
    #  p_slow_down叫做随机慢速的概率
    '''
    path = 5000.0 # 道路长度,每个元胞长度7m,因此道路长度模拟的是35km的一段
    n = 100 # 车辆数目
    v0 = 80 # 初始速度,高速公路不得低于60km/h
    ltv = 120 # 最大限速
    p = 0.3 # 减速概率
    rou = 0 # 自动车的比例
    times = 3000 # 模拟的时刻数目,每个时间单位代表现实世界当中的25.2s
    '''

    # x保存每辆车在道路上的位置，随机初始化
    x = np.random.randint(0,path,n)
    x.sort()
    # v保存每辆车的速度，初速度相同

    # 添加自动车的下标数组
    auto_list=np.random.randint(0,n-1,int(n*rou))

    v = np.ones((n,),dtype=int) * v0

    plt.figure(figsize=(5, 4), facecolor='w')
    # 模拟每个时刻

    for t in range(times):

        plt.scatter(x*7, [t*25.2] * n, s=1, c='k', alpha=0.05)
        # 模拟每辆车
        for i in range(n):
            # 计算当前车与前车的距离
            if x[(i + 1) % n] > x[i]:
                d = x[(i + 1) % n] - x[i]
            else:
                d = path - x[i] + x[(i + 1) % n]
            # 根据距离计算下一秒的速度


            temp_p_slow_down=p_slow_down
            if (auto_list == i).any():
                temp_p_slow_down=0
            if v[i] < d:
                if np.random.rand() > temp_p_slow_down:
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
    plt.xlim(0, path*7)
    plt.ylim(0, times*25.5)
    plt.xlabel(u'车辆位置m')
    plt.ylabel(u'模拟时间s')
    plt.title(u'交通模拟(车道长度%dm,车辆数%d,初速度%skm/h,减速概率%s)' % (path*7, n, v0, p_slow_down))

    plt.savefig('shikongtu.png')



def Run1d_withoutplot(path=5000, n=100, v0=60, ltv=120, p_wander=0, p_slow_down=0.3, rou=0, times=300):
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
    x = np.random.randint(0, path, n).astype('float64')
    x.sort()
    # v保存每辆车的速度，初速度相同

    # 添加自动车的下标数组
    auto_list = np.random.randint(0, n - 1, int(n * rou))

    v = np.ones(n) * v0


    # v_mean = np.zeros_like(v)

    q_num=0
    # 运行公路一段时间
    for t in range(times):
        # print(x[1])


        # 模拟每辆车的行为，包括自动车与普通车

        for i in range(n):


            # 计算当前车与前车的距离
            if x[(i + 1) % n] > x[i]:
                d = x[(i + 1) % n] - x[i]
            else:
                d = path - x[i] + x[(i + 1) % n]
            # 根据距离计算下一秒的速度


            # 自动车的行为是不会随机慢速
            temp_p_slow_down = p_slow_down

            if (auto_list == i).any():
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

        # if np.random.rand() < p_wander:
        #     v[i]-=1

        # 一秒后，车辆的位置发生了变化
        x += v

        # q_num是每个时间出车的数目，即流量

        q_sum_array=np.where(x>path,1,0)

        q_num +=np.sum(q_sum_array)

        # 注意,周期型边界条件
        x = x % path

        # v_mean+=v

    # v_mean/=times

    q_num/=times

    # q=np.mean(v_mean)

    return q_num



class Car:
    x=0
    y=0
    v=0


def Run2d_withoutplot(path=5000, n=200, v0=60, ltv=120,p_left_and_right=0.5,p_wander=0, p_slow_down=0.3, rou=0, times=300,p_huan=0.2):
    # 可以假设随机慢速均匀分布   p_slow_down叫做随机慢速
    '''
    path = 5000.0 # 道路长度
    n = 200 # 车辆数目
    v0 = 60 # 初始速度
    ltv = 120 # 最大限速
    p = 0.3 # 减速概率
    rou = 0 # 自动车的比例
    times = 3000 # 模拟的时刻数目
    '''

    # x保存每辆车在道路上的x轴位置坐标
    x = np.random.randint(0, path, n)
    x.sort()
    # 每辆车在道路上的y轴位置坐标随机给出
    y = np.random.binomial(1,p_left_and_right,size=n)

    #保存道路快照
    car_distribution = np.zeros((path,2))

    car_distribution[x,y]=1

    # 添加自动车的下标数组
    auto_list = np.random.randint(0, n, int(n * rou))
    # v保存每辆车的速度，初速度相同
    v = np.ones((n,),dtype=int) * v0



    # v_mean = np.zeros_like(v)

    q_num=0



    # 运行公路一段时间
    for t in range(times):

        # 模拟每辆车的行为，包括自动车与普通车

        for i in range(n):

            # x.sort()

            auto_flag=(auto_list == i).any()#为真是自动车

            
            # if x[(i + 1) % n] > x[i]:
            #     d = x[(i + 1) % n] - x[i]
            # else:
            #     d = path - x[i] + x[(i + 1) % n]


            # #首先进行特例的判断
            # if x[i]+d>path-1:


            #像人的视线一样计算当前车与前车的距离以及和另一个车道上前车的距离，如果另一个车道上前车距离更大那么有一定几率换道

            d1=1 #当前道路

            d2=1 #另一个道路

            while car_distribution[(x[i]+d1)%path,y[i]]==0 and d1<=120:

                d1=d1+1

            while car_distribution[(x[i]+d2)%path,1-y[i]]==0 and d2<=120:

                d2=d2+1

            
            if d2>d1:

                # 有一定几率按换道规则进行换道

                if np.random.rand()<p_huan:

                    y[i]=1-y[i]

                    d=d2

                else:

                    d=d1

            else:

                d=d1



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

        # if np.random.rand() < p_wander:
        #     v[i]-=1

        # 一秒后，车辆的位置发生了变化


        x += v

        # q_num是每个时间出车的数目，即流量

        q_sum_array=np.where(x>path,1,0)

        q_num +=np.sum(q_sum_array)

        # 周期型边界条件
        x = x % path

        # 更新快照
        car_distribution = np.zeros((path,2))

        car_distribution[x,y]=1


        # v_mean+=v

    # v_mean/=times

    q_num/=times

    # q=np.mean(v_mean)

    return q_num





