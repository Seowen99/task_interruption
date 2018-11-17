import rospy
from smach import State, StateMachine
from smach import Concurrence
from smach_ros import SimpleActionState
from plan_execution.msg import ExecutePlanGoal, ExecutePlanActionGoal
from bwi_tasks.common import states, task_machine
from bwi_kr_execution import goal_formulators
from move_base_msgs.msg import MoveBaseAction
import actionlib
import random


def run_concurrence(input_key):

	cc = Concurrence(outcomes=['succeeded', 'interrupted', 'aborted'],
				default_outcome = 'succeeded',
				input_keys=input_key,
				outcome_map={'interrupted':
					{ 'GENERATE_GOAL':'aborted',
					  'INTERRUPT_TASK':'interrupted'},
					'aborted': {'GENERATE_GOAL':'aborted',
					  'INTERRUPT_TASK':'continued'}})

	with cc:
	    Concurrence.add('GENERATE_GOAL', task_machine.generate_goal_based_task_sm(
				goal_formulators.GoToLocationName(), input_key))

	    Concurrence.add('INTERRUPT_TASK', Interrupt())
	    
	return cc

class Interrupt(State):
	def __init__(self):
		State.__init__(self, outcomes=['interrupted', 'continued'])
	
	def execute(self, userdata):
		
		randNum = random.randint(1, 11)
	
		if (randNum >= 1):
			client = actionlib.SimpleActionClient("/plan_executor/execute_plan",
				MoveBaseAction)
			client.wait_for_server()
			client.cancel_all_goals()
			return "interrupted"
			
		return "continued"

#def interrupt_task():
#	
#	randNum = random.randint(1, 11)
#	
#	if (randNum == 10):
#		client = actionlib.SimpleActionClient('/plan_executor/execute_plan',
#			ExecutePlanGoal)
#		client.wait_for_server()
#		client.cancelAllGoals()
#		return "interrupted"
#	return "continued"

#move interrupting concurrent state machine to contain generate_goal_based_task instead of
#GOTO_DOOR to make it a more general solution
#have interrupting state machine go to interrupting task and run it to completion
#upon completion of the interrupting task, return to the interrupted task and rerun/finish it
