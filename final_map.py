import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
import time
import os
import sys
import mod.write as write
import mod.calculate as cal

name = input("你要生成地图的文件名：")

dodification_path = sys.path[0] + "\\dodification\\" + name + ".csv" # path5
file_path = sys.path[0] + "\\raw_data\\" + name + ".csv" # path2
final_data = sys.path[0] + "\\answer\\n_" + name + ".csv" # path1
stop_point = sys.path[0] + "\\dodification\\" + name + ".xlsx" # path3
save_final_map_path = sys.path[0] + "\\final_map"
save_final_map_name = name + "_3.html"

data = pd.read_csv(file_path)
array = data.values
lat = array[:,4]#纬度
lng = array[:,3]#经度
Angle = array[:,2] #角度
Z = array[:,5]#点火1/熄火0
speed = array[:,11]#速度
t = array[:,10]#时间
m_t = []

for i in t:
    m_t.append(time.strptime(i, "%Y-%m-%d %H:%M:%S"))

c = float(input("请输入局部异常因子算法中异常点的比例："))

# AA00002中c = 0.05
# AB00006中c = 0.05
# AD00003中c = 0.05
# AD00013中c = 0.05
# AD00053中c = 0.05
# AD00083中c = 0.05
# AD00419中c = 0.05
# AF00098中c = 0.07
# AF00131中c = 0.05
# AF00373中c = 0.05

#修改完成图
locate = []
position = []
l = []
num = 0
sum = 0
line = write.get_line(dodification_path)

for i in range(1, len(lat) - 1):
    if abs(lat[i] - lat[i + 1]) + abs(lng[i] - lng[i + 1]) < 0.00037 and abs(lat[i] - lat[i - 1]) + abs(lng[i] - lng[i - 1]) < 0.00037:
        locate.append([lat[i], lng[i], int(time.mktime(m_t[i])), i])

cls = LocalOutlierFactor(n_neighbors = 190, contamination = c)
k = cls.fit_predict(locate)

for i in range(len(k)):
    if k[i] == 1:
        position.append(locate[i])

length = int(input("请输入异常点之间的分割长度："))

# AA00002中length = 300
# AB00006中length = 400
# AD00003中length = 500
# AD00013中length = 300
# AD00053中length = 700
# AD00083中length = 300
# AD00419中length = 300
# AF00098中length = 300
# AF00131中length = 100
# AF00373中length = 100

for i in range(len(position) - 1):
    if position[i + 1][2] - position[i][2] > 30 or abs(position[i][0] - position[i + 1][0]) + abs(position[i][1] - position[i + 1][1]) > 0.1:
        if len(l) > length:
            sum += write.writer(file_path, final_data, l)
            if num < line:
                sum += write.exchange(file_path, final_data, stop_point, i, num)
                num += 1
        l = []
    else:
        l.append(position[i])

write.map(final_data, cal.avg(lat), cal.avg(lng), os.path.join(save_final_map_path, save_final_map_name))

#输出每段路程的里程和平均速度
cal.cal(final_data)