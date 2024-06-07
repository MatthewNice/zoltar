#!/usr/bin/env python


import rospy
from std_msgs.msg import Float64, Int16, String, Bool
from sensor_msgs.msg import NavSatFix, TimeReference
from geometry_msgs.msg import Point, Twist
import traceback
import os
import sys
import requests
import time
import bisect
# import numpy as np
# import pandas as pd
# import shapely
# from shapely import LineString,Point
# from shapely.ops import nearest_points
# from shapely import Polygon
import json

velocity = 0.0
in_i24 = False
libpanda_controls_allowed = False
vsl_set_speed = 0
car_setpoint = 0

vsl_good = False

# velocity_topic = "vel"
velocity_topic = "/car/state/vel_x"
# gantry_topic = "/vsl/latest_gantry"

#controls allowed
libpanda_controls_allowed_topic = "/car/libpanda/controls_allowed"
zoltar_allowed_topic = "/zoltar_allowed"
zoltar_topic = "/zoltar"
#setpoint readers
# car_setpoint_topic = "v_ref"#"/pcm_cruise_2" #"/car/setpoint" #currently located at msg_467
car_setpoint_topic = "/acc/set_speed"
#vsl set speed
vsl_set_speed_topic = "/vsl/set_speed" ###this will need to change @######
#is i24
in_i24_topic = "/vsl/in_i24"
vsl_good_topic = "/vsl/vsl_good"


class vslmux:
    def __init__(self):
        rospy.init_node('vslmux', anonymous=True)

        self.pub_float = Float64()
        self.vsl_good = False
        self.libpanda_controls_allowed = False
        self.zoltar_allowed = False

        #map this to the desired speed topic
        self.mux_set_speed_pub = rospy.Publisher('/mux/set_speed', Float64, queue_size=1000)


        # rospy.Subscriber(in_i24_topic,Bool,self.in_i24_callback)
        rospy.Subscriber(libpanda_controls_allowed_topic,Bool,self.libpanda_controls_allowed_callback)
        rospy.Subscriber(vsl_set_speed_topic,Float64,self.vsl_set_speed_callback)
        rospy.Subscriber(car_setpoint_topic,Int16,self.car_setpoint_callback)
        rospy.Subscriber(velocity_topic,Float64,self.velocity_callback)
        rospy.Subscriber(vsl_good_topic,Bool,self.vsl_good_callback)
        rospy.Subscriber(zoltar_allowed_topic,Bool,self.zoltar_allowed_callback)
        rospy.Subscriber(zoltar_topic,Float64,self.zoltar_callback)

    def velocity_callback(self,data):
        # if not self.libpanda_controls_allowed:
        #     self.pub_float.data = data.linear.x#velocity
        #     self.mux_set_speed_pub.publish(self.pub_float)
        if not self.libpanda_controls_allowed:
            self.pub_float.data = data.data#velocity
            self.mux_set_speed_pub.publish(self.pub_float)
            
    def car_setpoint_callback(self,data):
        # if (self.libpanda_controls_allowed) & (not self.vsl_good):
        #     self.pub_float.data = data.linear.x#car_setpoint
        #     self.mux_set_speed_pub.publish(self.pub_float)
        if (self.libpanda_controls_allowed) & (not self.zoltar_allowed) & (not self.vsl_good):
            self.pub_float.data = data.data#car_setpoint
            self.mux_set_speed_pub.publish(self.pub_float)

    def vsl_set_speed_callback(self,data):
        if (self.libpanda_controls_allowed) & (not self.zoltar_allowed) & (self.vsl_good):
            self.pub_float.data = data.data #vsl_set_speed
            self.mux_set_speed_pub.publish(self.pub_float)

    def zoltar_callback(self,data):
        if (self.libpanda_controls_allowed) & (self.zoltar_allowed):
            self.pub_float.data = data.data#zoltar
            self.mux_set_speed_pub.publish(self.pub_float)

    def zoltar_allowed_callback(self,data):
        self.zoltar_allowed.data = data.data#zoltar_allowed

    def vsl_good_callback(self, data):
        self.vsl_good = data.data

    def libpanda_controls_allowed_callback(self,data):
        self.libpanda_controls_allowed = data.data



if __name__ == '__main__':
    try:
        head = vslmux()
        # head.loop()
        rospy.spin()
    except Exception as e:
        print(e)
        traceback.print_exc()
        print("An exception occurred")
