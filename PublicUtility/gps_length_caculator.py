#!/usr/bin/env python
# encoding: utf-8
'''
@summary: cacluate the length between two gps points
@author: xiuwen Yin
@change: 2018-03-05 create script
'''
from math import *

class CalcuateGpsLength(object):
    '''
    @summary: calcluate line total length which were composed by gps coordinates
    '''
    def __init__(self, value_list):
        self.value_list = value_list
    
    def haversine(self, lon1, lat1, lon2, lat2):
        '''
        @summary: calculate length between two gps points
        '''
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  # Convert decimal degrees to radians
        dlon = lon2 - lon1  # haversine formula
        dlat = lat2 - lat1  # haversine formula
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        
        r = 6371  # The average radius of the earth. Unit is kilometers
        
        return c * r * 1000
    
    def calc_gps_lenth(self, coordinates):
        '''
        @summary: calcuate coordinates's total length
        '''
        num = len(coordinates)
        distance_one_kml = 0.00
        
        for i in range(num - 1):  # points in coordinates
            distance_between_two_point = self.haversine(coordinates[i][0], coordinates[i][1], coordinates[i + 1][0], coordinates[i + 1][1])
            distance_one_kml += distance_between_two_point
        
        return distance_one_kml
    
    def get_coordinate_length(self, value_list=[]):
        '''
        @summary: get each gps line's longtitude and latitude and calclulate gps length
        '''
        coordinates = []
        total_length = 0.00
        
        for line in value_list:
            if line != '' and ',' in line:
                lon = line.split(',')[0]
                lat = line.split(',')[1]
                coordinates.append((float(lon), float(lat)))  
        total_length += self.calc_gps_lenth(coordinates)
        
        return total_length
