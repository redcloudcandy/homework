# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 21:21:13 2020

@author: tangyh
"""
import requests
import os
import jsonpath
import ujson 
from collections import defaultdict

class getData():
    def __init__(self, url: str, localHtmlFile:str):
        self.url = url
        self.localHtmlFile = localHtmlFile
        self.lines_info = {}
        self.lines_loop = {}
        self.stations_info = {}
        self.neighbor_info = defaultdict(list)
    def get_lines_stations_info(self):
        if os.path.exists(self.localHtmlFile):
            #html结果文件存在,直接读文件
            jsonObj = ujson.loads(open(self.localHtmlFile, encoding='utf-8').read())
            #print(jsonpath.jsonpath(jsonObj, '$.l[*].st[*].[n,sl]'))
            linesList = jsonpath.jsonpath(jsonObj,'$.l[*]')
            for line in linesList:
                lineName = jsonpath.jsonpath(line, '$.ln')[0]
                loopTag = jsonpath.jsonpath(line,'$.lo')[0]
                stations = []
                for station in jsonpath.jsonpath(line, '$.st[*]'):
                    stationName = str(jsonpath.jsonpath(station, '$.n')[0])
                    coordinate = tuple(map(float,str(jsonpath.jsonpath(station, '$.sl')[0]).split(',')))
                    #站点list
                    self.stations_info[stationName] = coordinate
                    
                    #线路添加站点
                    stations.append(stationName)
                
                self.lines_info[lineName] = stations
                self.lines_loop[lineName] = loopTag
            #print(len(self.lines_info))
            #print(len(self.stations_info))

        else:
            #html文件不存在，请求url保存结果文件
            r = requests.get(self.url)
            f = open(self.localHtmlFile,'w', encoding='utf-8')
            f.write(r.text)
            f.close()
    def get_neighbor_info(self):
        # 根据线路信息，建立站点邻接表dict
        def add_neighbor_dict(line, stationA, stationB):
            if strB == '':
                return
            if abs(line.index(stationA) - line.index(stationB)):
                #相邻站点
                if self.neighbor_info[stationA] :
                    self.neighbor_info[stationA].append(stationB)
                else:
                    self.neighbor_info[stationA] = [stationB]
        lines = self.lines_info.keys()
        for key in lines:                
            line = self.lines_info[key]
            for i in range(len(line)):
                if i == 0:
                    strA = line[0]
                    strB = line[1]
                    add_neighbor_dict(line, strA, strB)
                elif i == len(line)-1:
                    if self.lines_loop[key] == '1':
                        #环线，首尾两个车站也是相邻车站
                        self.neighbor_info[line[0]].append(line[i])
                        self.neighbor_info[line[i]].append(line[0])
                    else:
                        strA = line[i]
                        strB = line[i-1]
                        add_neighbor_dict(line, strA, strB)
                else:
                    strA = line[i]
                    strB = line[i-1]
                    add_neighbor_dict(line, strA, strB)
                    strB = line[i+1]
                    add_neighbor_dict(line, strA, strB)
#gc = getData('http://map.amap.com/service/subway?_1587041883235&srhdata=1100_drw_beijing.json','E://AIlearn//微软九步AI学习法-人工智能核心知识强化课程//homework//subway-beijing//subway_data.json')
#gc.get_lines_stations_info()
#gc.get_neighbor_info()
#print(gc.neighbor_info['西直门'])
#print(gc.neighbor_info['积水潭'])