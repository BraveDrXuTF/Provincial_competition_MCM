import matplotlib.pyplot as plt
import numpy as np
from CA import Run1d_withoutplot,Run2d_withoutplot,Run1d

from CAnet import RunCA_Net


# 单车道 限速-流量

for v in range(80, 111, 10):

    rou=np.linspace(0,1,10)

    for i in range(rou.shape[0]):

        q=Run1d_withoutplot(rou=rou[i],p_slow_down=0.5,ltv=v)

        plt.scatter(rou[i],q)


    plt.ylabel(u'流量(辆/25.2s)')
    plt.xlabel(u'自动驾驶车辆数占总车辆数比例')
    plt.title('v={}km/h'.format(v))
    plt.savefig('v{}.png'.format(v))
    plt.show()



# 双车道 限速-流量

for v in range(120, 121, 10):

    rou=np.linspace(0,1,10)

    for i in range(rou.shape[0]):

        q=Run2d_withoutplot(rou=rou[i],p_slow_down=0.5,ltv=v)

        plt.scatter(rou[i],q)


    plt.ylabel(u'流量(辆/25.2s)')
    plt.xlabel(u'自动驾驶车辆数占总车辆数比例')
    plt.title('v={}km/h'.format(v))
    plt.savefig('v{}_shuang.png'.format(v))
    plt.show()



# 网络 限速-流量

for v in range(80, 121, 10):

    rou=np.linspace(0,1,10)

    for i in range(rou.shape[0]):

        q=RunCA_Net(rou=rou[i],p_slow_down=0.5,ltv=v)

        plt.scatter(rou[i],q)


    plt.ylabel(u'流量(辆/25.2s)')
    plt.xlabel(u'自动驾驶车辆数占总车辆数比例')
    plt.title('v={}km/h'.format(v))
    plt.savefig('v{}_net.png'.format(v))
    plt.show()