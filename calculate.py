import pandas as pd
import time
from geopy.distance import vincenty

def dis(lat, lng):
    sum = 0
    for i in range(len(lat) - 1):
        sum += vincenty((lat[i], lng[i]), (lat[i + 1], lng[i + 1]), ellipsoid = 'WGS-84').km
    return sum

def avg(arr):
    a = 0
    for i in range(len(arr)):
        a += arr[i]
    return a / len(arr)

def dis(lat, lng):
    length = 0
    for i in range(len(lat) - 1):
        length += vincenty((lat[i], lng[i]), (lat[i + 1], lng[i + 1]), ellipsoid = 'WGS-84').km
    return length

def get_c(path):
    data = pd.read_csv(path)
    array = data.values
    Z = array[:,5]#点火1/熄火0
    t = array[:,10]#时间
    m_t = []
    pos = []
    for i in t:
        m_t.append(int(time.mktime(time.strptime(i, "%Y-%m-%d %H:%M:%S"))))

    for i in range(len(m_t) - 1):
        if Z[i] == 0 and Z[i + 1] == 1 and m_t[i + 1] - m_t[i] > 3600:
            pos.append(i)

    pos.append(len(m_t) - 1)

    return pos

def get_time(path, start, end):
    total_time = 0
    data = pd.read_csv(path, header = None)
    array = data.values
    acc = array[:, 5]
    t = array[:, 10]
    m_t = []
    flag = 1
    for i in t:
        m_t.append(int(time.mktime(time.strptime(i, "%Y-%m-%d %H:%M:%S"))))

    for i in range(start, end):
        if flag == 1:
            if acc[i + 1] == 1:
                if m_t[i + 1] - m_t[i] > 0:
                    total_time += m_t[i + 1] - m_t[i]
            else:
                flag = 0
        else:
            if acc[i + 1] == 0:
                flag = 1

    return total_time

def cal(path):
    pos = get_c(path)
    data = pd.read_csv(path, header = None)
    array = data.values
    lat = array[:,4]#纬度
    lng = array[:,3]#经度
    t = array[:,10]#时间
    speed = array[:,11]#速度
    m_t = []
    for i in t:
        m_t.append(int(time.mktime(time.strptime(i, "%Y-%m-%d %H:%M:%S"))))
    k = 0

    for i in range(len(pos)):
        rapid_acceleration = 0#急加速
        rapid_deceleration = 0#急减速
        for j in range(k, pos[i] - 1):
            if speed[j] - speed[j + 1] > 10:
                rapid_deceleration += 1
            elif speed[j + 1] - speed[j] > 10:
                rapid_acceleration += 1
        s = dis(lat[k:pos[i]],lng[k:pos[i]])
        ti = get_time(path, k, pos[i])
        k = pos[i] + 1
        sp = 3600 * s/ti
        print('第'+ str(i + 1) + '段行车里程：' + str(s))
        print('平均行车速度：' + str(sp))
        print('急加速次数：' + str(rapid_acceleration))
        print('急减速次数：' + str(rapid_deceleration))