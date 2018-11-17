import rospy
from smach import State, StateMachine
from smach import Concurrence
from smach_ros import SimpleActionState
from plan_execution.msg import ExecutePlanGoal, ExecutePlanActionGoal, ExecutePlanAction
from bwi_tasks.common import states, task_machine, visit_random_door
from bwi_kr_execution import goal_formulators
from std_msgs.msg import Empty, String
import actionlib
import random


def run_concurrence(goal, input_key):

	cc = Concurrence(outcomes=['succeeded', 'preempted', 'aborted'],
				default_outcome = 'succeeded',
				input_keys=input_key,
				outcome_map={'preempted':
					{ 'GENERATE_GOAL':'aborted',
					  'INTERRUPT_TASK':'preempted'},
					 'aborted': {'GENERATE_GOAL':'aborted',
					  'INTERRUPT_TASK':'continued'}})

	with cc:
	    Concurrence.add('GENERATE_GOAL', visit_random_door.GetRandomLocation())

	    Concurrence.add('INTERRUPT_TASK', Interrupt())
	    
	return cc

class Interrupt(State):
	def __init__(self):
		State.__init__(self, outcomes=['preempted', 'continued'])
	
	def execute(self, userdata):
		
		randNum = random.randint(1, 11)
	
		#if (randNum >= 1):
		#
		#	client = actionlib.SimpleActionClient("/plan_executor/execute_plan",
		#		ExecutePlanAction)
		#	#rospy.loginfo("before server")
		#	client.wait_for_server()
		#	#rospy.loginfo("after server")
		#	client.cancel_all_goals()
		#	#rospy.loginfo("after cancel")
		#	
		#	return "preempted"
			
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
