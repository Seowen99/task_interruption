import rospy
from smach import State, StateMachine
from smach import Concurrence
from smach_ros import SimpleActionState
from plan_execution.msg import ExecutePlanGoal, ExecutePlanActionGoal, ExecutePlanAction
from bwi_tasks.common import states, task_machine, actions_dictionary, task_stack
from bwi_kr_execution import goal_formulators
from std_msgs.msg import Empty, String
import actionlib
import random


def run_concurrence(goal):

	task_stack.TaskStack().add_to_stack(goal)

	cc = Concurrence(outcomes=['succeeded', 'preempted', 'aborted'],
				default_outcome = 'succeeded',
				child_termination_cb = child_term_cb,
				outcome_cb = out_cb)

	with cc:
	    Concurrence.add('GENERATE_GOAL', actions_dictionary.ActionDictionary().findAction(goal))

	    Concurrence.add('INTERRUPT_TASK', Interrupt(goal))
	
	#task_stack.TaskStack().remove_latest(goal)
	
	return cc
	
	
class Interrupt(State):
	def __init__(self, goal):
		State.__init__(self, outcomes=['preempted', 'continued']),
		self.goal = goal
	
	def execute(self, goal): 
# if goal is cancelled, add goal back to stack and then return that way the goal stays in the
# stack for later use
		
		raw_input("Press Enter to interrupt me.")
		
		client = actionlib.SimpleActionClient("/plan_executor/execute_plan",
				ExecutePlanAction)
		rospy.loginfo("before server")
		client.wait_for_server()
		rospy.loginfo("after server")
		client.cancel_all_goals()
		rospy.loginfo("after cancel")
			
		return "preempted"
		
		
def out_cb(outcome_map):
	if outcome_map['INTERRUPT_TASK'] == 'preempted':
		return 'preempted'
	elif outcome_map['GENERATE_GOAL'] == 'aborted':
		return 'aborted'
	else:
		return 'succeeded'
		

def child_term_cb(outcome_map):

	rospy.loginfo("child term")
	rospy.loginfo(outcome_map['INTERRUPT_TASK'])
	
	if outcome_map['INTERRUPT_TASK'] == 'preempted':
		rospy.loginfo("interrupt task cb")
		return True
		
	elif outcome_map['GENERATE_GOAL'] == 'succeeded':
		return True
		
	elif outcome_map['GENERATE_GOAL'] == 'aborted':
		return True
		
	return False	


