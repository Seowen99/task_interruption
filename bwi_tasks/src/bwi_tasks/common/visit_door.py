from bwi_tasks.common import task_machine
from bwi_kr_execution import goal_formulators, knowledge
import knowledge_representation
from smach import State
import rospy
import time

class VisitDoor(State):
    def __init__(self, door):
	State.__init__(self, outcomes=['preempted', 'aborted', 'succeeded'], output_keys=['location'])
	self.door = door
		
    def execute(self, userdata):
    	datathing = {"location": self.door}
    	userdata['location'] = self.door
	rospy.loginfo(datathing["location"])
	visit_door_sm = task_machine.generate_goal_based_task_sm(
		goal_formulators.GoToLocationName(), ['location'])
	
        result = visit_door_sm.execute(datathing)
        #time.sleep(6)
        return result
