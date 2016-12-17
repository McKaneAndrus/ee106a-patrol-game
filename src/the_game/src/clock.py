#!/usr/bin/env python
from rosgraph_msgs.msg import Clock
import rospy
import time
import rostime

if __name__ == '__main__':
	rospy.init_node("clock")
	clock = rospy.Publisher("clock", Clock, queue_size = 1)
	print "starting her up"
	print rospy.get_rostime()
	while not rospy.is_shutdown():
		curr =  rostime.Time.from_sec()
		clock.publish(Clock(curr))
		print "running her down"
		# # rospy.sleep(0.01)
		# secs += .01