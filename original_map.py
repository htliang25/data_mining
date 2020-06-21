import folium
import pandas as pd
import os
import sys
import mod.calculate as cal

# 测试地图包括一下10个
# AA00002
# AB00006
# AD00003
# AD00013
# AD00053
# AD00083
# AD00419
# AF00098
# AF00131
# AF00373

name = input("你要生成地图的文件名：")
file_path = sys.path[0] + "\\raw_data\\" + name + ".csv"
data = pd.read_csv(file_path)

array = data.values
lat = array[:,4]#纬度
lng = array[:,3]#经度

m = folium.Map([cal.avg(lat), cal.avg(lng)], zoom_start = 10)

#原图
location = list(zip(lat, lng))

route = folium.PolyLine(    #polyline方法为将坐标用线段形式连接起来
    location,    #将坐标点连接起来
    weight=3,  #线的大小为3
    color='green',  #线的颜色为绿色
    opacity=0.8    #线的透明度
).add_to(m)    #将这条线添加到刚才的区域m内

m.add_child(folium.LatLngPopup())
save_path = sys.path[0] + "\\original_map"
save_name = name + "_1.html"
m.save(os.path.join(save_path, save_name))

print("finish")