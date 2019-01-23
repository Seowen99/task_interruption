import rospy
from smach import State, StateMachine
from smach_ros import SimpleActionState
from plan_execution.msg import ExecutePlanGoal, ExecutePlanActionGoal, ExecutePlanAction
from bwi_tasks.common import states, task_machine, actions_dictionary, task_stack, null_task
from bwi_kr_execution import goal_formulators
from std_msgs.msg import Empty, String
import actionlib
import random
import time
import sys, select

### this class is completely redundant. It is never used

class Interrupt(State):
	def __init__(self, InterruptionManager):
		State.__init__(self, outcomes=['preempted', 'continued']),
#		self.goal = goal
		self.interruption_manager = InterruptionManager
		self.count = 0
		self.new_task = "NULL_TASK"
	
	# waits for input from the user
	# calls to get a new task and interrupt the current task if it gets input
	# waits until it is preempted by another state if no input is given
#	def execute(self, userdata): 
		
#		print "Hit any key to interrupt"
#		BLOCK_UNTIL_ANOTHER_FUNCTION_IS_CALLED
#		while (not self.preempt_requested()):
		
			#print "You have a second to answer!"
			
#			i, o, e = select.select( [sys.stdin], [], [], 1 )
#			if (i):
			
#				self.get_new_task()
				
#				self.interruption_manager.add_to_stack(self.interruption_manager.get_current_task())
				
#				self.interrupt_task()
				
#				return 'preempted'
			
#		print(self.interruption_manager.stack, " inside interruption_state after end")	
#		rospy.loginfo("preempt_requested by outside")
#		return 'continued'
		
	# gets the new task from the user and assigns it to an attribute
#	def get_new_task(self):
	
#		if (self.count % 3 == 0):
#			self.new_task = "GO_TO_JUSTIN"
#		elif (self.count % 3 == 1):
#			self.new_task = "GO_TO_JUSTIN"
#		elif (self.count % 3 == 2):
#			self.new_task = "GO_TO_420"
#		self.count += 1
#		self.new_task = "TEST_TASK"
			
	# adds current task to top of the stack
	# adds new task to the top of the stack
	# cancels current task and exits
	def interrupt_task(self):
	
		# adds current task back to the top of the stack
		self.interruption_manager.add_to_stack(self.interruption_manager.get_current_task())
		
		# adds the new task back to the top of the stack
		self.interruption_manager.add_to_stack(self.new_task)
	
		# cancels the current task so the GENERATE_GOAL	state in the interruption_manager
		# returns and the concurrent state machine can exit
#		client = actionlib.SimpleActionClient(
#			"/plan_executor/execute_plan", ExecutePlanAction)
#		rospy.loginfo("before server")
#		client.wait_for_server()
#		rospy.loginfo("after server")
#		client.cancel_all_goals()
#		rospy.loginfo("after cancel")
		
#		SELF.INTERRUPTING_TASK = THE_NEW_TASKING
		

