import rospy
from smach import State
from smach import Concurrence
from smach_ros import SimpleActionState
from plan_execution.msg import ExecutePlanActionGoal
from bwi_tasks.common import states, task_machine
from bwi_kr_execution import goal_formulators
import actionlib
import random

def run_concurrence():

	cc = Concurrence(outcomes=['succeeded', 'interrupted', 'aborted'],
				default_outcome = 'succeeded',
				input_keys=["location"],
				outcome_map={'interrupted':
					{ 'GOTO_DOOR':'aborted',
					  'INTERRUPT_TASK':'interrupted'},
					'aborted': {'GOTO_DOOR':'aborted',
					  'INTERRUPT_TASK':'continued'}})

	with cc:
	    Concurrence.add('GOTO_DOOR', task_machine.generate_goal_based_task_sm(
				goal_formulators.GoToLocationName(), ["location"]))

	    Concurrence.add("INTERRUPT_TASK", interrupt_task())


def interrupt_task():
	
	randNum = random.randint(1, 11)
	
	if (randNum == 10):
		client = actionlib.SimpleActionClient('/plan_executor/execute_plan/goal',
			ExecutePlanActionGoal)
		client.wait_for_server()
		client.cancelAllGoals()
		return 'interrupted'
	return 'continued'
