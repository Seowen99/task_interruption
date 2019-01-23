import rospy
from bwi_tasks.common import null_task, idle_task
from bwi_tasks.common import visit_door as vd

class ActionDictionary():
	def __init__(self, stackGUI):
		self.dict = {
			"GO_TO_JUSTIN": vd.VisitDoor("d3_402"),
			"GO_TO_PETER": vd.VisitDoor("d3_508"),
			"GO_TO_LAB": vd.VisitDoor("d3_414b1"),
#			"GO_TO_SEMINAR_ROOM": vd.VisitDoor("d3_516"),
#			"GO_TO_ROBOT_SOCCER_COURT": vd.VisitDoor("d4_436"),
			"GO_TO_400": vd.VisitDoor("d3_400"),
			"GO_TO_402": vd.VisitDoor("d3_402"),
			"GO_TO_404": vd.VisitDoor("d3_404"),
#			"GO_TO_414": vd.VisitDoor("d3_414a3"),
			"GO_TO_416": vd.VisitDoor("d3_416"),
			"GO_TO_420": vd.VisitDoor("d3_420"),
			"GO_TO_422": vd.VisitDoor("d3_422"),
			"GO_TO_430": vd.VisitDoor("d3_430"),
			"GO_TO_432": vd.VisitDoor("d3_432"),
#			"GO_TO_436": vd.VisitDoor("d3_436"),
			"GO_TO_500": vd.VisitDoor("d3_500"),
			"GO_TO_502": vd.VisitDoor("d3_502"),
			"GO_TO_508": vd.VisitDoor("d3_508"),
			"GO_TO_510": vd.VisitDoor("d3_510"),
			"GO_TO_512": vd.VisitDoor("d3_512"),
#			"GO_TO_516": vd.VisitDoor("d3_516"),
#			"GO_TO_600": vd.VisitDoor("d3_600"),
#			"GO_TO_710": vd.VisitDoor("d3_710a1"),
#			"GO_TO_816a": vd.VisitDoor("d3_816a"),
#			"GO_TO_824": vd.VisitDoor("d3_824"),
#			"GO_TO_ELEVATOR_EAST": vd.VisitDoor("d3_elev_east"),
#			"GO_TO_ELEVATOR_SOUTH": vd.VisitDoor("d3_elev_south"),
#			"GO_TO_ELEVATOR_WEST": vd.VisitDoor("d3_elev_west"),
#			"GO_TO_200": vd.VisitDoor("l3_200"),
#			"NULL_TASK": null_task.NullTask("NULL_TASK"),
			"IDLE_TASK": idle_task.IdleTask(stackGUI),
#			"TEST_TASK": null_task.NullTask("TEST_TASK")
		}
	
	def findAction(self, action):
		return self.dict[action]
		
	
