#!/usr/bin/python
import os
import math

g_light_level_list=[]
g_light_value_dict={}
g_new_light_value_list=[]
g_new_value_level_dict={}


def light_level_lowthres(backlight):
    for level in g_light_level_list[::-1]:
        if backlight >= level:
            return level

def light_level_highthres(backlight):
    for level in g_light_level_list:
        if backlight <= level:
            return level

def find_avail_backlight(value):#find cd value no more than standard and transmit to backlight
#    print "value is ",value
    for index in range(len(g_new_light_value_list)):
        if value < g_new_light_value_list[index]:
            if index == 0: 
                backlight="20"
            else:
                backlight=g_new_value_level_dict[g_new_light_value_list[index-1]]
            break
    else:
        backlight="255"
    print "---->",backlight
    return backlight

def light_level_interpolation():
    level_min=g_light_level_list[0]
    level_max=g_light_level_list[-1]
    for backlight in range(level_min,level_max+1):
        level_lthres=light_level_lowthres(backlight)
        level_hthres=light_level_highthres(backlight)
        value_lthres=g_light_value_dict[level_lthres]
        value_hthres=g_light_value_dict[level_hthres]
        if level_lthres == level_hthres:
            interpolation_value=value_lthres
        else:
            interpolation_value=(value_hthres-value_lthres)*float(backlight-level_lthres)/(level_hthres-level_lthres)+value_lthres

        print "%d:[%d,%d]--->%f" % (backlight,light_level_lowthres(backlight),light_level_highthres(backlight),interpolation_value)
        g_new_light_value_list.append(interpolation_value)
        g_new_value_level_dict[interpolation_value]=backlight
    print g_new_light_value_list
    print g_new_value_level_dict
    

def create_level_list():
    level_form_fp=open("light_level.txt","r")
    level_form_info=level_form_fp.readlines()
    for info in level_form_info:
        light_level=info.split()
        value=float(light_level[0])
        level=int(light_level[1])
        g_light_level_list.append(level)
        g_light_value_dict[level]=value

def standard_light_curve_synax():
    standard_form_fp=open("standard_light_curve.txt","r")
    standard_value_list=standard_form_fp.readlines()
    for level in range(len(standard_value_list)):
        standard_value_list[level]=standard_value_list[level].split()
    print standard_value_list,"+++++++++",len(standard_value_list)
    for row_level in standard_value_list:
        for col_value in row_level:
            find_avail_backlight(float(col_value))

create_level_list()
light_level_interpolation()
standard_light_curve_synax()
