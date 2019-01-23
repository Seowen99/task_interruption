import knowledge_representation
import smach_ros
import threading

from knowledge_representation import LongTermMemoryConduit
from smach import StateMachine, State

from bwi_tasks.common import interruption_manager, task_machine

class InterruptionThread(threading.Thread):

	def __init__(self, introspect, stack, stackGUI):
		threading.Thread.__init__(self)
		self._introspect = introspect
		
		self.ltmc = knowledge_representation.get_default_ltmc()

		task_machine.get_recover_from_failure_sm(self.ltmc)

		self.stack = stack

		self.interruptionManager = interruption_manager.InterruptionManager(self.stack, stackGUI)

		# Create top state machine
		self.sm = StateMachine(outcomes=['succeeded', 'preempted', 'aborted', 'continued'])
		# Open the container
		with self.sm:
			# Add states

			#	cc = interruption_state.run_concurrence("GO_TO_JUSTIN")
			StateMachine.add("RUN_STACK", self.interruptionManager,
				transitions={'succeeded':'RUN_STACK'})
			
	def run(self):
		if self._introspect:
			self.sis = smach_ros.IntrospectionServer('introspection_server', self.sm, '/SM_ROOT')
			self.sis.start()

		# Execute SMACH plan
		outcome = self.sm.execute()

		if self._introspect:
			rospy.spin()
			self.sis.stop()
