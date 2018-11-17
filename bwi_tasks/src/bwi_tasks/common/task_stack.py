import rospy

class TaskStack():
	def __init__(self):
		self.stack = []
	
	def add_to_stack(self, task):
		self.stack.append(task)
	
	def remove_latest(self, task):
		self.stack.pop()

	#def current_task(self):
		
