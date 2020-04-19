# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 21:29:11 2020

@author: tangyh
搜索路径
"""
import pandas as pd
# 画地铁图
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import getData as gg




class searchPath():
    def __init__(self, data: dir,station: dir ,neighbor_info: list, start: str, destination: str, by_way=[]):
        self.lines_info = data
        self.station = station
        self.neighbor_info = neighbor_info
        self.from_station = start
        self.to_station = destination
        self.by_way = by_way
        self.visted = set()
    def drawSubway(self):
        # 如果汉字无法显示，请参照
        subway_graph = nx.Graph()
        
        matplotlib.rcParams['font.sans-serif'] = ['SimHei'] 
        plt.figure(figsize=(80,80)) #设置画布大小
        subway_graph.add_nodes_from(list(self.station.keys()))
        
        #nx.draw(subway_graph, self.station, with_labels=True, node_size=50)
        
        neighbor_info_graph = nx.Graph(self.neighbor_info)
        nx.draw(neighbor_info_graph,self.station,with_labels=True,node_size=50)
        # matplotlib.arams['font.family']='sans-serif'
    def get_path_DFS_ALL(self,lines_info, neighbor_info, from_station, to_station):
        # 递归算法，本质上是深度优先
        # 遍历所有路径
        # 这种情况下，站点间的坐标距离难以转化为可靠的启发函数，所以只用简单的DFS算法
        # 检查输入站点名称
        
        
        if from_station not in neighbor_info or to_station not in neighbor_info:
            return '站点输入错误,请重输'
        return
        need_serach = [from_station]
        pathes = [[from_station]]       
        viested = set()
        
        while pathes:
            path = pathes.pop(-1)
            #neighbor = neighbor_info[path]
            froniter = path[-1]
            
            if froniter in viested:continue
            
            next_station = neighbor_info[froniter]
            
            for station in next_station:
                if station in path:continue
                
                new_path = path + [station]
                
                pathes.append(new_path)
                
                if station == to_station:
                    return new_path
            viested.add(froniter)
        
        
    def get_next_station_DFS_ALL(self,node, neighbor_info, to_station):
        
        #1、当前node的相邻站点列表中有目的地车站(to_station)，则停止搜索
        #2、当前node的相邻站点列表不含有目的地车站(to_station)，则将当前列表加入到节点列表中，继续遍历
        
        '''返回从起点到终点的1条路线，可能不包含终点站'''
        result = []
        if node in self.visted:return []
        self.visted.add(node)
        
        if to_station in neighbor_info[str(node)]:
            result.append(node)
            result.append(to_station)
            return result
        else:
            result.append(node)
            result += self.get_next_station_DFS_ALL(neighbor_info[str(node)].pop(-1), neighbor_info, to_station)
        return result    
            
        
    #  你也可以使用第二种算法：没有启发函数的简单宽度优先
    def get_path_BFS(lines_info, neighbor_info, from_station, to_station):
        # 搜索策略：以站点数量为cost（因为车票价格是按站算的）
        # 这种情况下，站点间的坐标距离难以转化为可靠的启发函数，所以只用简单的BFS算法
        # 由于每深一层就是cost加1，所以每层的cost都相同，算和不算没区别，所以省略
        # 检查输入站点名称
        pass
    
    # 你还可以用第三种算法：以路径路程为cost的启发式搜索
    def get_path_Astar(lines_info, neighbor_info, stations_info, from_station, to_station):
        # 搜索策略：以路径的站点间直线距离累加为cost，以当前站点到目标的直线距离为启发函数
        # 检查输入站点名称
        pass
    def is_goal():
        #Shortest Path Priority
        pass
    def get_successor():
        #Minimum Transfer Priority
        pass
    def strategy():
        #Comprehensive Priority
        pass
gc = gg.getData('http://map.amap.com/service/subway?_1587041883235&srhdata=1100_drw_beijing.json','E://AIlearn//微软九步AI学习法-人工智能核心知识强化课程//homework//subway-beijing//subway_data.json')
gc.get_lines_stations_info()
gc.get_neighbor_info()
sea = searchPath(gc.lines_info, gc.stations_info, gc.neighbor_info, '', '')
#sea.drawSubway()
#print(sea.neighbor_info['苹果园'])
print(sea.get_next_station_DFS_ALL( '回龙观', sea.neighbor_info, '生命科学园' ))
