#!/usr/bin/env python
import tf
import rospy
import numpy as np

from geometry_msgs.msg import Vector3, Twist
import exp_quat_func as eqf
import ar_tag_subs as ats

from game2 import get_coord, get_steps

class ZumyController():

    def __init__(self, zumy, zumy_ar):
        self.ar_tags = {'self': 'ar_marker_' + str(zumy_ar), 'origin':'ar_marker_0'}
        self.listener = tf.TransformListener()
        self.zumy_vel = rospy.Publisher('%s/cmd_vel' % zumy, Twist, queue_size=2)
        self.rate = rospy.Rate(1000)
        self.step_x, self.step_y = game2.get_steps()

    def go_to_waypoint(self, waypoint):
        #waypoint array-like (x,y)
        angle = 0
        is_aligned = False
        at_waypoint = False

        while not rospy.is_shutdown() and not at_waypoint:
            try:
                (trans_ab, rot_ab) = self.listener.lookupTransform(self.ar_tags['player'], self.ar_tags['origin'], rospy.Time(0))
                (trans_ba, rot_ba) = self.listener.lookupTransform(self.ar_tags['origin'], self.ar_tags['player'], rospy.Time(0))
            except Exception as e:
                print e
                V = Vector3(0,0,0)
                W = Vector3(0,0,0)
                twist = Twist(V,W)
                self.zumy_vel.publish(twist)
                continue

            x_curr = trans_ba[0]/self.step_x
            y_curr = trans_ba[1]/self.step_y

            g_ab = ats.return_rbt(trans_ab,rot_ab)

            trans_bc = np.array([self.step_x*waypoint[0], self.step_y*waypoint[1], 0.0])
            omega_bc = np.array([0.0, 0.0, 1.0])
            zumy_vec = trans_bc - trans_ba
            angle = np.arctan2([zumy_vec[1]], [zumy_vec[0]])
            g_bc = eqf.create_rbt(omega_bc, angle, trans_bc)

            #print g_ab, g_bc

            g_ac = np.dot(g_ab, g_bc)
            v, w = ats.compute_twist(g_ac)

            if abs(w[2]) < 0.03*np.pi:
                is_aligned = True
            
            if abs(waypoint[0] - x_curr) < 0.1 and abs(waypoint[1] - y_curr) < 0.1:
                V = Vector3(0,0,0)
                W = Vector3(0,0,0)
                at_waypoint = True
            elif not is_aligned: # Rotate until aligned
                V = Vector3(0,0,0)
                W = Vector3(w[0],w[1],w[2])
            else:
                V = Vector3( (v[0]/abs(v[0])) * min(abs(v[0]), 0.07),v[1],v[2])
                W = Vector3(w[0],w[1],1.6*w[2]) # scalar coeff to speed up response

            twist = Twist(V,W)
            self.zumy_vel.publish(twist)

        return 1

    def get_position(self):
        return get_coord(self.ar_tags['self'])

    def get_orientation(self):
        return get_orientation(self.ar_tags['self'])

    def get_state(self):
        return (self.get_position(), self.get_orientation())