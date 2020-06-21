import csv
import pandas as pd
import folium
import datetime
import change as change
import calculate as cal

def get_line(path):
    k = 0

    with open(path, 'r', encoding = 'utf-8-sig') as f:
       while f.readline() != '':
           k += 1

    return (k - 2)/2

def create_map(path, location):

    #写新文件
    f = open(path, 'w', newline = '',encoding = 'utf-8-sig')
    writer = csv.writer(f, dialect = 'excel')

    l = []
    for i in range(len(location)):
        l.append([i, location[i][0], location[i][1]])
        writer.writerow(l[i])

    f.close()

def writer(read_path, write_path, l):

    #读原文件
    file = open(read_path)
    reader = csv.reader(file)
    rows = [row for row in reader]

    #写新文件
    f = open(write_path, 'a', newline = '',encoding = 'utf-8-sig')
    writer = csv.writer(f, dialect = 'excel')

    for i in range(len(l)):
        s = l[i][3]
        writer.writerow(rows[s])

    lat = []
    lng = []

    for i in range(len(l)):
        lat.append(l[i][0])
        lng.append(l[i][1])

    lat = list(lat)
    lng = list(lng)

    f.close()
    file.close()
    return cal.dis(lat, lng)

def exchange(read_path, write_path, change_path, pos, k):

    #读原文件
    file = open(read_path)
    reader = csv.reader(file)
    rows = [row for row in reader]

    #写新文件
    f = open(write_path, 'a', newline = '',encoding = 'utf-8-sig')
    writer = csv.writer(f, dialect = 'excel')

    #打开修正文件
    change_loc = pd.read_excel(change_path, sheet_name = k, header = None)
    array = change_loc.values
    position = array[:, 0]
    lat = []
    lng = []
    location = []

    for i in position:
        lat.append(float(i.split(',', 3)[1]))
        lng.append(float(i.split(',', 3)[0]))
    for i in range(len(lat)):
        location.append(change.gcj02_to_wgs84(lng[i], lat[i]))

    length = cal.dis(lat, lng)
    if len(lat) > 2:
        a = datetime.datetime.strptime(rows[i + pos][10], "%Y-%m-%d %H:%M:%S")
        b = datetime.datetime.strptime(rows[i][10], "%Y-%m-%d %H:%M:%S")
        total_time = (a - b).seconds
        speed = int(3600 * length/total_time)
    else:
        speed = int(rows[pos - 2][11])

    for i in range(len(lat)):
        r = [rows[i + pos][0], rows[i + pos][1], rows[i + pos][2], location[i][1], location[i][0], rows[i + pos][5], rows[i + pos][6], rows[i + pos][7], rows[i + pos][8], rows[i + pos][9], rows[i + pos][10], speed, rows[i + pos][12]]
        writer.writerow(r)

    f.close()
    file.close()
    return length

def map(path, latitude, longtitude, save_path):
    data = pd.read_csv(path)
    array = data.values
    l = list(zip(array[:, 4], array[:, 3]))
    m = folium.Map([latitude, longtitude], zoom_start = 10)
    route = folium.PolyLine(    #polyline方法为将坐标用线段形式连接起来
        l,    #将坐标点连接起来
        weight=3,  #线的大小为3
        color='green',  #线的颜色为绿色
        opacity=0.8    #线的透明度
    ).add_to(m)    #将这条线添加到刚才的区域m内
    m.save(save_path)