#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from mavros_msgs.msg import OverrideRCIn, CommandBool
import mavros
#from mavros.msg import State, Battery

class JoyController(object):
	def __init__(self):
		rospy.init_node("joystick_node")
		self.axes = []
		self.buttons = []
		self.twist = [0, 0, 0, 0, 1500, 1500, 1500, 1500]
		self.throttle = 1500
		self.x = 1500
		self.y = 1500
		self.yaw = 1500
		self.armed = False
		self.pub = rospy.Publisher("/rc/override", OverrideRCIn, queue_size=10)
		s = rospy.ServiceProxy("/cmd/arming", CommandBool)
		#s1 = rospy.Service("/set_mode", mavros, setState)
		rospy.Subscriber("/joy", Joy, self.processJoy) 
		#rospy.Subscriber("/state", State, self.getState)
		#rospy.Subscriber("/battery", Battery, self.getBattery)

		r = rospy.Rate(10)
		while not rospy.is_shutdown():
			self.printJoy()
			self.s(True)
			r.sleep()

	def getState(self, msg):
		self.armed = msg.armed

	def getBattery(self, msg):
		print 'battery level: ', msg

	def processJoy(self, msg):
		if msg.buttons[2]:
			self.armed = False
		if msg.buttons[3]:
			self.armed = True
		self.axes = msg.axes
		self.buttons = msg.buttons
		self.x = 1500+self.axes[0]*300 
        self.y = 1500+self.axes[1]*300 
		self.throttle = 1500+msg.axes[3]*300
		self.yaw = 1500+msg.axes[2]*-300
		if self.armed:
            (self.twist[0], self.twist[1], self.twist[2], self.twist[3]) = (int(self.x), int(self.y), int(self.z), int(self.yaw))

	def printJoy(self):
		print 'buttons: ', self.buttons
		#print 'axes: ', self.axes
		print 'armed: ', self.armed
		print 'throttle: ', self.throttle
		print 'yaw: ', self.yaw
			
if __name__ == '__main__':
	control = JoyController()
	rospy.spin()