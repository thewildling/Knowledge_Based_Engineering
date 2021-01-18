import random
import time

import NXOpen
from AnalyzerForNode import Analyzer

analyze = True

# Opening the DFAfile

theSession = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work
displayPart = theSession.Parts.Display
workPart.RuleManager.Reload(True)

markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Add New Child Rule")

workPart.RuleManager.CreateDynamicRule("root:", "Node", "Child", "{\n Class, Node_finished; \n}", None)

nErrs1 = workPart.RuleManager.DoKfUpdate(markId1)

# Starting the analyzer

if analyze:
    a = Analyzer("test_fem_", "C:\\Users\\Marianne Pettersen\\Desktop\\auto\\femsims\\")
    a.getSolidBodies()
    a.createFEM("7.3", "0.73", "Aluminum_5086")
    a.defineSim()
    a.assignConstrain(1, 5)
    a.assignConstrain(1, 15)
    a.assignLoad(5000, 1, 12, [0, 1, 0])
    a.assignLoad(5000, 1, 13, [0, -1, 0])
    a.assignTorqueLoad(2000, 1, 11)
    a.assignTorqueLoad(2000, 1, 14)
    a.solveSim()

    """ time.sleep(5)

    a.openResults()
    a.runAnimation()
    global rand
    rand = str(random.randint(1, 1000))

    a.saveAnimGIF("C:\\Users\\Marianne Pettersen\\PycharmProjects\\Automatisering\\Node_project\\", "result" + ".gif")

    theNxMessageBox = NXOpen.UI.GetUI().NXMessageBox
    theNxMessageBox.Show("Bodies", NXOpen.NXMessageBoxDialogType.Information, "Solve 1 ferdig")
 
	Underneath is the code-part we would have implemented to create the loop for checking the stress.
	
	approvedStress = a.checkStress()

	#Looping through the max nodal stress and expanding the node-diameter by 5 while the max-stress is too high
	while not approvedStress:
		node_diameter += 5
		MyHandler.updateDesign(node_diameter, hole_diameter, cutting_radius)
		a = Analyzer("test_fem_", "C:\\Users\\Marianne Pettersen\\Desktop\\auto\\femsims\\")
		a.getSolidBodies()
		a.createFEM("7.3", "0.73", "Aluminum_5086")
		a.defineSim()
		a.assignConstrain(1, 5)
		a.assignConstrain(1, 15)
		a.assignLoad(force, 1, 12, [0, 1, 0])
		a.assignLoad(force, 1, 13, [0, -1, 0])
		a.assignTorqueLoad(torque, 1, 11)
		a.assignTorqueLoad(torque, 1, 14)
		a.solveSim()
		approvedStress = a.checkStress()"""
