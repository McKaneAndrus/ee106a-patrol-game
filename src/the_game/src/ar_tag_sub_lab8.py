#!/usr/bin/env python
import tf
import rospy
import sys
import math
import numpy as np
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Transform, Vector3
from kalman_zumy.srv import NuSrv

listener = None

if __name__=='__main__':
    rospy.init_node('ar_tags_subs')
    if len(sys.argv) < 3:
        print('Use: ar_tag_subs_lab8.py [ origin AR tag number ] [ zumy AR tag number ]')
        sys.exit()
    ar_tags = {}
    ar_tags['ar0'] = 'ar_marker_' + sys.argv[1]
    ar_tags['arZ'] = 'ar_marker_' + sys.argv[2]

    listener = tf.TransformListener()
    send_data = rospy.ServiceProxy('innovation', NuSrv)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (trans, rot) = listener.lookupTransform(ar_tags['ar0'], ar_tags['arZ'], rospy.Time(0))
            transform = Transform()
            transform.translation = trans
            transform.rotation = rot
            send_data(transform, ar_tags['ar0'])
        except:
            print ''

        rate.sleep()
