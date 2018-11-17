import rospy
from bwi_tasks.common import visit_random_door, visit_lab_door, visit_justin_door

class ActionDictionary():
	def __init__(self):
		self.dict = {
			"GO TO JUSTIN DOOR": visit_justin_door.JustinLocation(),
			"GO TO LAB DOOR": visit_lab_door.LabLocation()
		}
	
	def findAction(self, action):
		return self.dict[action]
		
	
