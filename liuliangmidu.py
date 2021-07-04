import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from CA import Run1d_withoutplot,Run2d_withoutplot,Run1d

from CAnet import RunCA_Net

# 单车道 流量密度2
plt.figure(figsize=(5, 4), facecolor='w')
for n in range(1,1000,10):

    q=Run1d_withoutplot(n=n,p_slow_down=0.5)

    plt.scatter(n/35,q)


plt.ylabel(u'辆/25.2s')
plt.xlabel(u'辆/km')
plt.savefig('2_dan.png')
plt.show()






# 双车道 流量密度2
plt.figure(figsize=(5, 4), facecolor='w')
for n in range(1, 1000, 10):
    q = Run2d_withoutplot(n=n, p_slow_down=0.5)

    plt.scatter(n / 35, q)

plt.ylabel(u'流量(辆/25.2s)')
plt.xlabel(u'密度(辆/km)')
plt.savefig('2_shuang.png')
plt.show()




# 交通网 流量密度2
plt.figure(figsize=(5, 4), facecolor='w')
for n in range(1, 300, 20):
    q = RunCA_Net(n=n, p_slow_down=0.5)

    plt.scatter(n / 35, q)


plt.ylabel(u'流量(辆/25.2s)')
plt.xlabel(u'密度(辆/km)')
plt.savefig('2_net.png')
plt.show()