#!/usr/bin/env python
import tf
import rospy
import sys
import math
import numpy as np
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Transform, Vector3
import kin_func_skeleton as kfs
import exp_quat_func as eqf
from exp_quat_func import quaternion_to_exp as q2e
from exp_quat_func import create_rbt as rbt
from exp_quat_func import compute_gab as gab

lkp = {} # dictionary containing the last known position of AR tags
combos = []

def callback(msg, ar_tags):
    for i in range(0, len(msg.transforms)):

        # YOUR CODE HERE
        # The code should look at the transforms for each AR tag
        # Then compute the rigid body transform between AR0 and AR1, 
        # AR0 and ARZ, AR1 and ARZ
        #  hint: use the functions you wrote in exp_quat_func
        #  note: you can change anything in this function to get it working
        #  note: you may want to save the last known position of the AR tag 

        lkp[msg.transforms[i].child_frame_id] = msg.transforms[i].transform # position / orientation
    
    if len(lkp) == 3:
        exps = {ar_tag: q2e(q2v(lkp[ar_tag].rotation)) for ar_tag in ar_tags.values()}
        rbts = {tag: rbt(exps[tag][0], exps[tag][1], v2v(lkp[tag].translation)) for tag in ar_tags.values()}
        g2g = dict()
        for combo in combos:
            g2g[combo] = gab(rbts[combo[0]], rbts[combo[1]])
        print g2g
 
def q2v(quat):
    return np.array([quat.x, quat.y, quat.z, quat.w])

def v2v(vec):
    return np.array([vec.x, vec.y, vec.z])

if __name__=='__main__':
    rospy.init_node('ar_tags_subs_manual')
    if len(sys.argv) < 4:
        print('Use: ar_tags_subs_manual.py [ AR tag number ] [ AR tag number ] [ AR tag number ] ')
        sys.exit()
    ar_tags = {}
    ar_tags['ar0'] = 'ar_marker_' + sys.argv[1]
    ar_tags['ar1'] = 'ar_marker_' + sys.argv[2]
    ar_tags['arZ'] = 'ar_marker_' + sys.argv[3]
    combos = [(ar_tags['ar0'],ar_tags['ar1']),(ar_tags['ar0'],ar_tags['arZ']),(ar_tags['ar1'],ar_tags['arZ'])]

    rospy.Subscriber('/tf', TFMessage, callback, ar_tags)
    rospy.spin()
