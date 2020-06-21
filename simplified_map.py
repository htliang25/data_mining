import folium
import pandas as pd
import os
import time
from sklearn.neighbors import LocalOutlierFactor
import sys
import change as change
import write as write
import calculate as cal

name = input("你要生成地图的文件名：")
file_path = sys.path[0] + "\\raw_data\\" + name + ".csv"
data = pd.read_csv(file_path)

array = data.values
lat = array[:,4]#纬度
lng = array[:,3]#经度
Angle = array[:,2] #角度
Z = array[:,5]#点火1/熄火0
speed = array[:,11]#速度
t = array[:,10]#时间
m_t = []
location = []
for i in t:
    m_t.append(time.strptime(i, "%Y-%m-%d %H:%M:%S"))

m = folium.Map([cal.avg(lat), cal.avg(lng)], zoom_start = 10)

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

#删减图
locate = []
position = []
l = []
num = 1

for i in range(1, len(lat) - 1):
    if abs(lat[i] - lat[i + 1]) + abs(lng[i] - lng[i + 1]) < 0.00037 and abs(lat[i] - lat[i - 1]) + abs(lng[i] - lng[i - 1]) < 0.00037:
        locate.append([lat[i], lng[i], int(time.mktime(m_t[i])), i])

cls = LocalOutlierFactor(n_neighbors = 190, contamination = c)
k = cls.fit_predict(locate)

for i in range(len(k)):
    if k[i] == 1:
        position.append(locate[i])

location = []

length = input("请输入异常点之间的分割长度")

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
        if len(l) > 300:
            route = folium.PolyLine(    #polyline方法为将坐标用线段形式连接起来
                l,    #将坐标点连接起来
                weight=3,  #线的大小为3
                color='red',  #线的颜色为红色
                opacity=0.8    #线的透明度
            ).add_to(m)    #将这条线添加到刚才的区域m内
            folium.Marker(l[0], popup = str(num) + '\n' + str(change.wgs84_to_gcj02(l[0][1], l[0][0])), icon = folium.Icon(color = 'red')).add_to(m)
            location.append(change.wgs84_to_gcj02(l[0][1], l[0][0]))
            folium.Marker(l[len(l) - 1], popup = str(num) + '\n' + str(change.wgs84_to_gcj02(l[len(l) - 1][1], l[len(l) - 1][0])), icon = folium.Icon(color = 'green')).add_to(m)
            location.append(change.wgs84_to_gcj02(l[len(l) - 1][1], l[len(l) - 1][0]))
            num += 1
        l = []
    else:
        l.append([position[i][0], position[i][1]])

save_outliers = sys.path[0] + "\\outliers\\" + name + ".csv"
save_simplified_map_path = sys.path[0] + "\\simplified_map"
save_simplified_map_name = name + "_2.html"

write.create_map(save_outliers, location)
m.save(os.path.join(save_simplified_map_path, save_simplified_map_name))
print("finish")