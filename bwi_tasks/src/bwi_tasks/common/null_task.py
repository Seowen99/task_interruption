import rospy
import time
from smach import State

class NullTask(State):
	def __init__(self, task_name):
		State.__init__(self, outcomes=['succeeded'])
		self._task_name = task_name
		
	def execute(self, userdata):
		print(self._task_name + "\n")
		time.sleep(5)
		print(self._task_name + "DONE\n")
		return 'succeeded'
