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
import time
import sys, select


def run_concurrence(goal):

	task_stack.TaskStack().add_to_stack(goal)

	cc = Concurrence(outcomes=['succeeded', 'preempted', 'aborted'],
				default_outcome = 'succeeded',
				outcome_map = {'succeeded':{'GENERATE_GOAL':'succeeded'},
					'preempted':{'INTERRUPT_TASK':'preempted'},
					'aborted':{'GENERATE_GOAL':'aborted'}},
				outcome_cb = out_cb,
				child_termination_cb = child_term_cb)

	rospy.loginfo(cc._child_termination_cb)

	with cc:
	    Concurrence.add('GENERATE_GOAL', 
	    	actions_dictionary.ActionDictionary().findAction(goal))

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
		
		print "Hit any key to interrupt"
		while (not self.preempt_requested()) :
		
			#print "You have a second to answer!"
			
			i, o, e = select.select( [sys.stdin], [], [], 1 )
			if (i):
				client = actionlib.SimpleActionClient(
					"/plan_executor/execute_plan", ExecutePlanAction)
				rospy.loginfo("before server")
				client.wait_for_server()
				rospy.loginfo("after server")
				client.cancel_all_goals()
				rospy.loginfo("after cancel")	
				return 'preempted'
				
		rospy.loginfo("preempt_requested by outside")
		return 'continued'
		
		
def out_cb(outcome_map):
	if outcome_map['INTERRUPT_TASK'] == 'preempted':
		return 'preempted'
	elif outcome_map['GENERATE_GOAL'] == 'aborted':
		return 'aborted'
	else:
		return 'succeeded'
		

def child_term_cb(outcome_map):

	#return ['INTERRUPT_TASK']

	rospy.loginfo("child term")
	rospy.loginfo(outcome_map['INTERRUPT_TASK'])
	rospy.loginfo(outcome_map['GENERATE_GOAL'])
	
	if outcome_map['INTERRUPT_TASK'] == 'preempted':
		rospy.loginfo("interrupt task cb")
		return True
		
	elif outcome_map['GENERATE_GOAL'] == 'succeeded':
		rospy.loginfo("generate goal cb")
		return True
		
	elif outcome_map['GENERATE_GOAL'] == 'aborted':
		rospy.loginfo("generate goal abort")
		return True
		
	return False	


