from mttkinter import mtTkinter as tk
import threading
from bwi_tasks.common import actions_dictionary as ad
from plan_execution.msg import ExecutePlanGoal, ExecutePlanActionGoal, ExecutePlanAction
import rospy
import actionlib

class StackGUI(threading.Thread):
	def __init__(self, stack):
		threading.Thread.__init__(self)
		self.stack = stack
		self.action_dict = ad.ActionDictionary(self)
		self.current_task = "IDLE_TASK"
		self.interrupted = False
		
	def buildGui(self):
		root = tk.Tk()
		self._root = root
		self.stack_labels = []
#		self.stack = ["This1", "snack", "hello_world", "Is this working?"]

		self._root.winfo_toplevel().title("Task Manager")
	
		# contains the buttons with the different tasks a user can assign
		self.leftFrame = tk.Frame(root)
		
		# contains the frames that hold the labels with each previously-assigned
		# task in the stack in them
		self.rightFrame = tk.Frame(root)
	
		# putting a header on the side with the stack inside
		label = tk.Label(self.rightFrame, text = "Stack:", width = 10, underline = 6, justify = tk.CENTER)
		label.pack()
		
		self.populateStackLabels()
	
		# iterates through the actions dictionary and adds all the

		# currently-implemented tasks to the rightFrame as buttons
		
#		self.count = -1
		self.action_stack = []
		
#		for key in self.action_dict.dict:
#			print(key + " is the key being added")
#			self.action_stack.append(key)
#			self.count += 1
#			button = tk.Button(self.leftFrame, text = key, width = 10, 
#				command = lambda: self.interruptTask(self.action_stack[self.count]))
#			button.pack()
#			print(key + " was added")

	

		for key in sorted(self.action_dict.dict):
			self.action_stack.append(key)
#			print("I appended " + key)

		# creates buttons for all the actions in the actions_dictionary
		# can't loop currently becasue it retains the last key put in
		# as the parameter for the interruptTask method
		button = tk.Button(self.leftFrame, text = self.action_stack[0], width = 10,
			command = lambda: self.interruptTask(self.action_stack[0]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[1], width = 10,
			command = lambda: self.interruptTask(self.action_stack[1]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[2], width = 10,
			command = lambda: self.interruptTask(self.action_stack[2]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[3], width = 10,
			command = lambda: self.interruptTask(self.action_stack[3]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[4], width = 10,
			command = lambda: self.interruptTask(self.action_stack[4]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[5], width = 10,
			command = lambda: self.interruptTask(self.action_stack[5]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[6], width = 10,
			command = lambda: self.interruptTask(self.action_stack[6]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[7], width = 10,
			command = lambda: self.interruptTask(self.action_stack[7]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[8], width = 10,
			command = lambda: self.interruptTask(self.action_stack[8]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[9], width = 10,
			command = lambda: self.interruptTask(self.action_stack[9]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[10], width = 10,
			command = lambda: self.interruptTask(self.action_stack[10]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[11], width = 10,
			command = lambda: self.interruptTask(self.action_stack[11]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[12], width = 10,
			command = lambda: self.interruptTask(self.action_stack[12]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[13], width = 10,
			command = lambda: self.interruptTask(self.action_stack[13]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[14], width = 10,
			command = lambda: self.interruptTask(self.action_stack[14]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[15], width = 10,
			command = lambda: self.interruptTask(self.action_stack[15]))
		button.pack()
		
		button = tk.Button(self.leftFrame, text = self.action_stack[16], width = 10,
			command = lambda: self.interruptTask(self.action_stack[16]))
		button.pack()
		
#		button = tk.Button(self.leftFrame, text = self.action_stack[17], width = 10,
#			command = lambda: self.interruptTask(self.action_stack[17]))
#		button.pack()
		
#		button = tk.Button(self.leftFrame, text = self.action_stack[18], width = 10,
#			command = lambda: self.interruptTask(self.action_stack[18]))
#		button.pack()
		
		
#		button = tk.Button(self.leftFrame, text = "Hello!", width = 10, command = lambda: self.hello(root))
#		button.pack()

#		button = tk.Button(self.leftFrame, text = "Quit!", width = 10, command = root.destroy)
#		button.pack()

		# packs the leftFrame and rightFrame to their side of the interface
		self.leftFrame.pack(side=tk.LEFT)
		self.rightFrame.pack(side=tk.RIGHT)
	
	
	def hello(self, root):
		print("Hello!")
		self.clearAndRepopulateStack()
	
	# assigns current_task to the last stack_label and adds it back to stack_labels
	# to keep it consistent with the labels displayed
	def getCurrentTask(self):
		self.current_task = self.stack_labels.pop()
		self.stack_labels.append(self.current_task)
		self.current_task = self.current_task.cget("text")
	
	# empties the stack and resets the stack_labels attribute
	# calls populateStackLabels to repopulate the stack with the new keys
	def clearAndRepopulateStack(self):
	
		for x in self.stack_labels:
			x.destroy()
			self.stack_labels = []
			
		self.populateStackLabels()
		
	# populates rightFrame with labels containing the keys in the stack	
	def populateStackLabels(self):
		for x in self.stack:
			label = tk.Label(self.rightFrame, text = x, background = "white", justify = tk.CENTER)
			self.stack_labels.append(label)
			label.pack()
	
	def run(self):
		self.buildGui()
		self._root.mainloop()
		
	
	# if the task hasn't been interrupted once already for the current task,
	# then this adds the new task's key to the stack, turns interrupted to
	# true to prevent multiple interruptions of the same task, and
	# cancels all goals published so the goal-accomplishing state machine
	# moves on to the new task in the stack without finishing the old task
	def interruptTask(self, key):
		if (not self.interrupted):
			self.getCurrentTask() # not used here. Why do we need this?
			self.stack.append(key)
			self.interrupted = True
		
			client = actionlib.SimpleActionClient(
				"/plan_executor/execute_plan", ExecutePlanAction)
#			rospy.loginfo("before server")
			client.wait_for_server()
#			rospy.loginfo("after server")
			client.cancel_all_goals()
#			rospy.loginfo("after cancel")

#def main():
	#stackGUI = StackGUI()
	#stackGUI.start()
	
	
#if __name__ == "__main__":
#	main()
