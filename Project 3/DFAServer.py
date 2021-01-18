
# Stores the path to DFAServer working directory
pathToApp = "C:\\Users\\Marianne Pettersen\\Desktop\\auto\\DFA's\\"

# Read the templates content of the template file
f1 = open(pathToApp + "Templates\\Curved_Rail_temp.dfa", "r")
dataGeneral = f1.read()
print("data from template GENERAL:", dataGeneral)

f2 = open(pathToApp + "Templates\\Curved_Rail_line.dfa", "r")
dataLine = f2.read()
print("data from template LINE:", dataLine)

f3 = open(pathToApp + "Templates\\Curved_Rail_curve.dfa", "r")
dataCurve = f3.read()
print("data from template CURVE:", dataCurve)

# Emulate the input data for S-rail.
first_straight_length = 6000
second_straight_length = 3000
third_straight_length = 3000

first_curve_radius = 2000
second_curve_radius = 2000

x = 0
y = 0
z = 0

#Now update the templates and generate the final result.
data = dataGeneral.replace("<GLOBAL_X>", str(x)) # data was initialized from dataGeneral...
data = data.replace("<GLOBAL_Y>", str(y))
data = data.replace("<GLOBAL_Z>", str(z))

#Insert path elements - here it is "just" hardcoded for the trial
#First segment
pathElements = dataLine.replace("<ID>", "1")
pathElements = pathElements.replace("<START_X>", str(x))
pathElements = pathElements.replace("<START_Y>", str(y))
pathElements = pathElements.replace("<START_Z>", str(z))
pathElements = pathElements.replace("<END_X>", str(x))
pathElements = pathElements.replace("<END_Y>", str(y + first_straight_length))
pathElements = pathElements.replace("<END_Z>", str(z))

#Second segment
pathElements = pathElements + dataCurve.replace("<ID>", "2")
pathElements = pathElements.replace("<CURVE_RADIUS>", str(first_curve_radius))
pathElements = pathElements.replace("<START_ANG>", "0") #NB! Constant to be replaced.
pathElements = pathElements.replace("<END_ANG>", "180") #NB! Constant to be replaced.
pathElements = pathElements.replace("<CENTER_X>", str(x-first_curve_radius))
pathElements = pathElements.replace("<CENTER_Y>", str(y + first_straight_length))
pathElements = pathElements.replace("<CENTER_Z>", str(z))

#Third element
pathElements = pathElements + dataLine.replace("<ID>", "3")
pathElements = pathElements.replace("<START_X>", str(x-2*first_curve_radius))
pathElements = pathElements.replace("<START_Y>", str(y + first_straight_length))
pathElements = pathElements.replace("<START_Z>", str(z))
pathElements = pathElements.replace("<END_X>", str(x-2*first_curve_radius))
pathElements = pathElements.replace("<END_Y>", str(y + first_straight_length - second_straight_length))
pathElements = pathElements.replace("<END_Z>", str(z))

#Fourth element
pathElements = pathElements + dataCurve.replace("<ID>", "4")
pathElements = pathElements.replace("<CURVE_RADIUS>", str(second_curve_radius))
pathElements = pathElements.replace("<START_ANG>", "180") #NB! Constant to be replaced.
pathElements = pathElements.replace("<END_ANG>", "360") #NB! Constant to be replaced.
pathElements = pathElements.replace("<CENTER_X>", str(x-first_curve_radius-second_curve_radius*2))
pathElements = pathElements.replace("<CENTER_Y>", str(y + first_straight_length - second_straight_length))
pathElements = pathElements.replace("<CENTER_Z>", str(z))

#Fifth element (See the movie)
pathElements = pathElements + dataLine.replace("<ID>", "5")
pathElements = pathElements.replace("<START_X>", str(x-2*first_curve_radius-2*second_curve_radius))
pathElements = pathElements.replace("<START_Y>", str(y + first_straight_length - second_straight_length))
pathElements = pathElements.replace("<START_Z>", str(z))
pathElements = pathElements.replace("<END_X>", str(x-2*first_curve_radius-2*second_curve_radius))
pathElements = pathElements.replace("<END_Y>", str(y + first_straight_length - second_straight_length + third_straight_length))
pathElements = pathElements.replace("<END_Z>", str(z))

#Now insert the path elements to the common template
data = data.replace("<PATH_ELEMENTS>", pathElements)

#Insert the vars for path elements - by this time we know what are
#those - <PATH_ELEMENTS_VARS>
pathElementsVars = "line_rail_path_1:,curve_rail_path_2:, line_rail_path_3:, curve_rail_path_4:,line_rail_path_5:"
data = data.replace("<PATH_ELEMENTS_VARS>", pathElementsVars)

print(data)

#Write the results to the common file
f = open(pathToApp + "A_Curved_rail.dfa", "w")
f.write(data)
f.close()
