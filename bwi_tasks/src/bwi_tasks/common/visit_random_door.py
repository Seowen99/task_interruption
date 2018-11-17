from bwi_tasks.common import task_machine
from bwi_kr_execution import goal_formulators, knowledge
import knowledge_representation
from smach import State
import rospy

class GetRandomLocation(State):
    def __init__(self):
	State.__init__(self, outcomes=['preempted', 'continued', 'aborted', 'succeeded'])
        self.ltmc = knowledge_representation.get_default_ltmc()
		
    def execute(self, userdata):
    	datathing = {}
	knowledge.GetRandomBwiLocation(self.ltmc).execute(datathing)
	rospy.loginfo(datathing["location"])
	visit_door_sm = task_machine.generate_goal_based_task_sm(
		goal_formulators.GoToLocationName(), ["location"])
	
        visit_door_sm.execute(datathing)
        return 'succeeded'
