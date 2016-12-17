#!/usr/bin/env python
import tf
import rospy
import numpy as np
from the_game.msg import Vector2
from geometry_msgs.msg import Vector3, Twist
import exp_quat_func as eqf
import ar_tag_subs as ats
import sys, traceback

# from game2 import get_coord, get_steps

class ZumyController:

    def __init__(self, zumy, zumy_ar, grid_x = 9, grid_y = 6):
        # rospy.init_node('zumy_%s_controller' % (zumy))

        self.ar_tags = {'self': 'ar_marker_' + str(zumy_ar), 'origin':'ar_marker_0'}
        self.listener = tf.TransformListener()
        self.zumy_vel = rospy.Publisher('%s/cmd_vel' % zumy, Twist, queue_size=2)
        self.rate = rospy.Rate(1000)
        self.step_x, self.step_y = 0.14, 0.14
        self.grid_x = grid_x
        self.grid_y = grid_y
        rospy.Subscriber("step_messages", Vector2, self.step_callback)

    def step_callback(self, message):
        # Update step_sizes from grid_broadcaster
        self.step_x, self.step_y = message.x, message.y

    def go_to_waypoint(self, waypoint, interrupt):
        #waypoint array-like (x,y)
        angle = 0
        is_aligned = False
        at_waypoint = False


        while not rospy.is_shutdown() and not at_waypoint and not interrupt[0]:
            try:
                (trans_ab, rot_ab) = self.listener.lookupTransform(self.ar_tags['self'], self.ar_tags['origin'], rospy.Time(0))
                (trans_ba, rot_ba) = self.listener.lookupTransform(self.ar_tags['origin'], self.ar_tags['self'], rospy.Time(0))
            except Exception as e:
                # print e
                # traceback.print_exc(file=sys.stdout)
                # print e.traceback()
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
            v = np.reshape(v, (3,))
            # print v, type(v)

            if abs(w[2]) < 0.03*np.pi:
                is_aligned = True
            
            if abs(waypoint[0] - x_curr) < 0.16 and abs(waypoint[1] - y_curr) < 0.16:
                V = Vector3(0,0,0)
                W = Vector3(0,0,0)
                at_waypoint = True
            elif not is_aligned: # Rotate until aligned
                V = Vector3(0,0,0)
                W = Vector3(w[0],w[1],w[2])
            else:
                V = Vector3( (v[0]/abs(v[0])) * min(abs(v[0]), 0.05),v[1],v[2])
                W = Vector3(w[0],w[1],1.4*w[2]) # scalar coeff to speed up response

            twist = Twist(V,W)
            # print "publishing ", twist
            self.zumy_vel.publish(twist)

        if interrupt[0]:
            print "INTERRRRUUUPPPTTTTEEEEEEED"
            V = Vector3(0,0,0)
            W = Vector3(0,0,0)
            twist = Twist(V,W)
            # print "publishing ", twist
            self.zumy_vel.publish(twist)
        return 1

    # def get_position(self):
    #     return get_coord(self.ar_tags['self'], self.step_x, self.step_y)

    # def get_orientation(self):
    #     return get_orientation(self.ar_tags['self'])

    def get_coord(self):

        done = False
        while not done:
            # print "getting coord" 
            try:
                (trans, rot) = self.listener.lookupTransform(self.ar_tags['origin'], self.ar_tags['self'], rospy.Time(0))
                done = True
            except Exception as e:
                # print e
                continue
            x_coord = int(round(trans[0]/self.step_x))
            y_coord = int(round(trans[1]/self.step_y))
            if x_coord > self.grid_x or y_coord > self.grid_y or x_coord + y_coord == 0 or x_coord < 0 or y_coord < 0:
                done = False
                print "Player out of bounds?"
        print "self at ", x_coord, y_coord
        return x_coord, y_coord

    def get_coord_of(self, tag):

        done = False
        while not done:
            # print "getting coord" 
            try:
                (trans, rot) = self.listener.lookupTransform(self.ar_tags['origin'], 'ar_marker_' + tag, rospy.Time(0))
                done = True
            except Exception as e:
                # print e
                continue
            x_coord = int(round(trans[0]/self.step_x))
            y_coord = int(round(trans[1]/self.step_y))
            if x_coord > self.grid_x or y_coord > self.grid_y or x_coord + y_coord == 0 or x_coord < 0 or y_coord < 0:
                done = False
                print "Patrol tag {} out of bounds?".format(tag)
        print "tag at ", x_coord, y_coord
        return x_coord, y_coord

    #test dis
    def get_orientation(self):
        done = False
        while not done: 
            try:
                (trans, rot) = self.listener.lookupTransform(self.ar_tags['origin'], self.ar_tags['self'], rospy.Time(0))
                done = True
            except:
                continue
            g_ab = ats.return_rbt(trans,rot)
            angle = np.arctan2(g_ab.item((1,0)), g_ab.item((0,0)))  
            print angle * 180/np.pi  
            diff = np.array([0, np.pi/2, np.pi, 3*np.pi/2]) - (angle if angle >= 0 else 2 * np.pi + angle) 
            orientations = {0:(1,0), 1:(0,1), 2:(-1,0), 3:(0,-1)}
            # print "self"
            # print diff * 180/np.pi
            # print orientations
            # print np.argmin(abs(diff))
            return orientations[np.argmin(abs(diff))]

    def get_orientation_of(self, tag):
        done = False
        while not done: 
            try:
                (trans, rot) = self.listener.lookupTransform(self.ar_tags['origin'], 'ar_marker_' + tag, rospy.Time(0))
                done = True
            except:
                continue
            g_ab = ats.return_rbt(trans,rot)
            angle = np.arctan2(g_ab.item((1,0)), g_ab.item((0,0)))  
            # print "tag", tag
            # print angle * 180/np.pi  
            diff = np.array([0, np.pi/2, np.pi, 3*np.pi/2]) - (angle if angle >= 0 else 2 * np.pi + angle) 
            # print "post", diff * 180/np.pi
            orientations = {0:(1,0), 1:(0,1), 2:(-1,0), 3:(0,-1)}
            # print orientations
            # print np.argmin(abs(diff))
            return orientations[np.argmin(abs(diff))]

    def get_state(self):
        return (self.get_coord(), self.get_orientation())