import rospy
from smach import State, StateMachine
from smach import Concurrence
from bwi_tasks.common import states, task_machine, task_stack, null_task, interruption_state
from bwi_tasks.common import actions_dictionary
from bwi_kr_execution import goal_formulators
from std_msgs.msg import Empty, String
import random
import time
import sys, select


class InterruptionManager(State):
	def __init__(self, stack, stackGUI):
		State.__init__(self, outcomes=['succeeded'])
		
		# holds the string keys for all the queued tasks
		self.stack = stack
		
		self.stackGUI = stackGUI
		
		# holds the string key for the latest task on the stack
		# changes when a new task is assigned or one is finished
		self.current_task = "IDLE_TASK"
		
		self.interrupt = interruption_state.Interrupt(self)
		self.action_dict = actions_dictionary.ActionDictionary(self.stackGUI)
		#self.GUI = interface.Interface(self.interrupt, self.action_dict)

	
	
	# assigns the task on top of the stack to the current task
	# runs the concurrent state machine to accomplish the task
	def execute(self, userdata):
	
		self.userdata = userdata
	
#		self.stack.append("NULL_TASK")
#		print(self.stack)
		
		self.assign_current_task()
#		print(self.stack, " after assignment")
#		print(self.current_task)
		#self.run_concurrence()
		
		self.complete_goal()
		
		if (not self.stackGUI.interrupted):
			self.remove_top_of_stack()

#		print(self.stack, " after completion/interruption")
#		time.sleep(1)
		
		self.stackGUI.clearAndRepopulateStack()
		self.stackGUI.interrupted = False
#		print("stack cleared and repopulated")
		
		return 'succeeded'
		
		
	# pops the last thing off the stack and makes it the current task
	def assign_current_task(self):
		self.current_task = self.stack.pop()
		self.stack.append(self.current_task)
		
		
	# adds the given task to the top of the stack
	def add_to_stack(self, task):
		self.stack.append(task)
		
		
	# pops the last thing off the stack without returning the value
	def remove_top_of_stack(self):
		self.stack.pop()
		
		
	### redundant. self.current_task can be accessed in other ways
	### this is never used
	# returns the current task for the manager
	def get_current_task(self):
		return self.current_task
		
	
	def complete_goal(self):
	
		sm = StateMachine(outcomes = ['succeeded', 'preempted', 'aborted'])
		
		with sm:
			StateMachine.add("GENERATE_GOAL", 
				self.action_dict.findAction(self.current_task), 
					transitions={'succeeded':'succeeded'})
						
		sm.execute()

	### redundant code. this method is never reached, interruption state is
	### never used
	# creates a concurrent state machine that completes a goal and waits to inerrupt it
	# returns the outcome of the state machine
	def run_concurrence(self):
		
#		print(self.get_current_task())

		cc = Concurrence(outcomes=['succeeded', 'preempted', 'aborted'],
					default_outcome = 'succeeded',
					outcome_map = {
						'succeeded':{'GENERATE_GOAL':'succeeded'}},
					child_termination_cb = self.child_term_cb)

#		rospy.loginfo(cc._child_termination_cb)

		with cc:
#		    Concurrence.add('GENERATE_GOAL', 
#		    	actions_dictionary.ActionDictionary().findAction(self.get_current_task()))

			# gets class associated with the given task
			# executes the class and completes the task
			Concurrence.add('GENERATE_GOAL',
		    		self.action_dict.findAction(self.current_task))

			# runs the interface to get new tasks from the user
			Concurrence.add('INTERRUPT_TASK', interruption_state.Interrupt(self))
	
		return cc.execute()




	### redundant method since run_concurrence is redundant
	def child_term_cb(self, outcome_map):

		#return ['INTERRUPT_TASK']

	#	rospy.loginfo("child term")
	#	rospy.loginfo(outcome_map['INTERRUPT_TASK'])
	#	rospy.loginfo(outcome_map['GENERATE_GOAL'])

		try:
			if outcome_map['INTERRUPT_TASK'] == 'succeeded':
		#		rospy.loginfo("interrupt task cb")
				return True
		
			elif outcome_map['GENERATE_GOAL'] == 'succeeded':
		#		print("I am in the callback")
		#		self.GUI.root.destroy()
		#		print("GUI should be destroyed")
		#		rospy.loginfo("generate goal cb")
				return True
			
		except KeyError:
			return False
		
	#	elif outcome_map['GENERATE_GOAL'] == 'aborted':
	#		rospy.loginfo("generate goal abort")
	#		return True
		
		return False	


