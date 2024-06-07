#!/usr/bin/env python3

# print("Drop 25 cents here..")

# wish = input("--Zoltar says: MAKE YOUR WISH--")
# print("ZOLTAR SPEAKS")
# print("Your Wish is Granted")

#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64, Int16, String, Bool
from geometry_msgs.msg import PointStamped
from sensor_msgs.msg import NavSatFix, TimeReference
import traceback
import os
import sys
import time
import requests
import time
import bisect
import numpy as np
import pandas as pd
# import shapely
# from shapely import LineString,Point
# from shapely.ops import nearest_points
# from shapely import Polygon
import json

velocity_topic = "/car/state/vel_x"
sport_mode_topic = "car/state/sport_mode"
eco_mode_topic = "car/state/eco_mode"
v_pr_topic = "/vsl/ego_radar/prevailing_speed"
# gantry_topic = "/vsl/latest_gantry"
vsl_set_speed_topic = "/vsl/set_speed"
distance_lines_topic="/acc/set_distance"
zoltar_request_topic="/zoltar_request"

highbeams_topic="/highbeams"

# gantry = None
vsl_set_speed = None
social_limit_v = 0
base_social_limit = 2
distance_lines = 0
max_speed = 32 ##32 m/s is 71.6 mph
velocity = None
# radar0,radar1,radar2,radar3,radar4,radar5,radar6,radar7 = None,None,None,None,None,None,None,None
# radar8,radar9,radar10,radar11,radar12,radar13,radar14,radar15 = None,None,None,None,None,None,None,None
# radar_state = [[],[],[],[]]#nested list, x, y, relv,time
sport_mode=0
eco_mode=0
normal=0
v_pr = 0
highbeams=0
zoltar_request=0

def sport_mode_callback(data):
    global sport_mode
    sport_mode=data.data

def eco_mode_callback(data):
    global eco_mode
    eco_mode=data.data

def gantry_callback(data):
    global gantry
    gantry = data.data

def velocity_callback(data):
    global velocity
    velocity = data.data

def v_pr_callback(data):
    global v_pr
    v_pr = data.data

def vsl_set_speed_callback(data):
    global vsl_set_speed
    vsl_set_speed = data.data

def distance_lines_callback(data):
    global distance_lines
    # global base_social_limit
    # global social_limit_v
    distance_lines = data.data
    # if distance_lines >0:
    #     social_limit_v = base_social_limit*distance_lines
    # else:
    #     social_limit_v = base_social_limit #the acc system is not on
    # # print('Social limit is: ',social_limit_v)

def highbeams_callback(data):
    global highbeams
    highbeams = data.data

def zoltar_request_callback(data):
    global zoltar_request
    zoltar_request = data.data

timeLimit = 5
recentflips = [] #timestamps of bit flips within the last timeLimit seconds
last = 0
zoltar_allowed = False

def doubleClick():
    global highbeams
    now = highbeams

    global last
    global zoltar_allowed
    global sport_mode

    if (now != last) & (now == 0): #the 1 to 0 transition implies the highbeams have been flipped on
        #this is where we track a new flip
        recentflips.append(time.time())

    if (len(recentflips) >= 2) & (sport_mode == 1):
        zoltar_allowed = True
    else:
        zoltar_allowed = False
        zoltar_request = 0 #resetting the zoltar_request value

    #clean up
    recursivePop() #clean up older flips
    last = now

def recursivePop():
    global recentflips
    global timeLimit
    if len(recentflips) !=0:
        oldest_time = recentflips.pop(0)
        #print(oldest_time, time.time())
        if abs(oldest_time - time.time()) > timeLimit:
            recentflips.pop(0) #pop the oldest flip time
            recursivePop()
        else:
            recentflips.insert(0,oldest_time)
    else:
        return

class zoltar:
    def __init__(self):
        rospy.init_node('zoltar', anonymous=True)

        # rospy.Subscriber(gantry_topic,Int16,gantry_callback)
        rospy.Subscriber(velocity_topic,Float64,velocity_callback)
        rospy.Subscriber(vsl_set_speed_topic,Float64,vsl_set_speed_callback)
        rospy.Subscriber(distance_lines_topic,Int16,distance_lines_callback)
        rospy.Subscriber(sport_mode_topic,Bool,sport_mode_callback)
        rospy.Subscriber(eco_mode_topic,Bool,eco_mode_callback)
        rospy.Subscriber(v_pr_topic,Float64,v_pr_callback)
        rospy.Subscriber(zoltar_request_topic,Float64,zoltar_request_callback)

        # TODO: subscribe to the offset value (should always be 2m/s in zoltar_allowed)

        # TODO add publishers for /zoltar and /zoltar_allowed
        global zoltar_allowed_pub
        zoltar_allowed_pub = rospy.Publisher('/zoltar_allowed',Bool,queue_size=1000)
        global zoltar_pub
        zoltar_pub = rospy.Publisher('/zoltar',Float64,queue_size=1000)
        global zoltar_request_pub
        zoltar_request_pub = rospy.Publisher('/zoltar_request',Float64,queue_size=1000)

        self.rate = rospy.Rate(20)

    def loop(self):
        while not rospy.is_shutdown():
            try:
                # global max_speed
                # global social_limit_v
                # global middle_set_speed_pub
                # global vsl_set_speed
                # global velocity
                # global sport_mode
                # global eco_mode
                # global normal
                # global base_social_limit
                global v_pr
                global highbeams
                global zoltar_allowed
                global zoltar_request


                doubleClick()
                zoltar_allowed_pub.publish(zoltar_allowed)

                if zoltar_request == 0:
                    v_zoltar_user = velocity #when there is no zoltar request yet
                else:
                    v_zoltar_user = zoltar_request

                social_limit_v = 2
                zoltar_pub.publish(min(max(v_pr-social_limit_v, v_zoltar_user), max_speed))


            except Exception as e:
                print(e)
                traceback.print_exc()
                print("Something has gone wrong.")
            self.rate.sleep()

if __name__ == '__main__':
    try:
        head = zoltar()
        head.loop()
    except Exception as e:
        print(e)
        traceback.print_exc()
        print("An exception occurred")
