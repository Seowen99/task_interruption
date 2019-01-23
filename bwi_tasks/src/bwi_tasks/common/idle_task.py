from bwi_tasks.common import task_machine
from bwi_kr_execution import goal_formulators, knowledge
import knowledge_representation
from smach import State
import rospy
import time

class IdleTask(State):
    def __init__(self, stackGUI):
		State.__init__(self, outcomes=['succeeded'], output_keys=['location'])
		self.stackGUI = stackGUI
		
    def execute(self, userdata):
    	while (not self.stackGUI.interrupted):
    		time.sleep(1)
        return 'succeeded'
