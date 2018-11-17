from bwi_tasks.common import task_machine
from bwi_kr_execution import goal_formulators, knowledge
import knowledge_representation
from smach import State
import rospy
import time

class JustinLocation(State):
    def __init__(self):
	State.__init__(self, outcomes=['preempted', 'continued', 'aborted', 'succeeded'])
		
    def execute(self, userdata):
    	datathing = {"location": "d3_402"}
	rospy.loginfo(datathing["location"])
	visit_door_sm = task_machine.generate_goal_based_task_sm(
		goal_formulators.GoToLocationName(), ["location"])
	
        result = visit_door_sm.execute(datathing)
        #time.sleep(6)
        return 'succeeded'
