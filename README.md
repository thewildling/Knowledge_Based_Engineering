# Knowledge_Based_Engineering
This repository includes all projects completed by my team during the course *TMM4275 Knowledge-base Engineering* at NTNU. Videos of all projects can be found in the Video-folder.

## Project 1 ##

This project task involved creating a KBE system for a chair-manufacturing company. The idea was to create a solution that allowed the customer to define different specifications of the chair (height, lenght of feet, thickness, color etc.), and then present the finished design to the user without the user needing any engineering/programming skills. The solution would design the chair in Siemes NX automatically based on only a few parameters from the customer input. This solution was created for 2 specific users: the customer and the process engineer. The reason for creating a UI for the process engineer as well was that the factory would have limits on their equipment, and thereby limits on the chairs that could be made. 

### Setup ###

Design a basic chair-template in a .dfa-file. Initialize an apache web server, running locally on the computer. Add the OWL-file to the server. 
Start the Python-files called *DFAServer* and *ManufReqServer*. Have NX running on the computer. After the userinput has been submitted, press update on the DFA-file inside NX to see the updated chair.  

### User stories ###

The customer:
1. The customer enters *127.0.0.1:1234/productConfig*. 
2. He/she enters the wanted specifications for the chair and presses the submit button.
3. The customer then enters the info-page on *127.0.0.1:1234/info*. 
4. Here the customer can see the specifications of their chair, and whether or not the chair can be made depending on the manufacturing limits. 

The process engineer:
1. The process engineer enters the website *127.0.0.1:4321/process*.
2. He enters the maximum and minimum boundaries based on the machinery making the chair.
3. He/she then presses the submit-button to send the requirements to the fuseki-server.  

 #### GUI ####
 
We did not focus on design of the user interface in this project, so the design is very simple and created with HTML-code.
The GUI for the process engineer is the window on the left, where he/she define limits for the chair. The middle window is the window for which the customer chooses the desired sizes and colors of the chair. The window on the right is just a simple info-page where the order information is repeated to the customer as well as a confirmation that the product can be made (is within the limits).
![alt text](https://github.com/thewildling/Knowledge_Based_Engineering/blob/main/Pictures/GUI-Chair.png?raw=true)

The image below is the result (chair-design) in NX.
![alt text](https://github.com/thewildling/Knowledge_Based_Engineering/blob/main/Pictures/GUI-ChairInNX.png?raw=true)


### Sequence Diagram ###

![alt text](https://github.com/thewildling/Knowledge_Based_Engineering/blob/main/Pictures/Sequence%20diagram%20-%20Chair.png?raw=true)

### Architecture ###

![alt text](https://github.com/thewildling/Knowledge_Based_Engineering/blob/main/Pictures/Architecture%20-%20Chair.png?raw=true)

Walk through of the Architecture:

1. The product designer constructs a .dfa-file to work as a template.
2. The process engineer enters the website *127.0.0.1:4321/process*, and sets the constraints for the design space (machinery). This is hosted by the Manufacturing request server.
3. The constraints are sent via the Manufacturing request server to a Apache Jenna Fuseki server online, where a query is used to insert them in the correct place in the OWL file. 
4. The customer then enters the website under *127.0.0.1:1234/productConfig*, and is asked to put in the measurements of the desired product. This is hosted by the DFA-server.
5. The DFA-server connects to the fuseki-server and sends a query to retrieve the max/min constraints. The DFA-server checks if the customer's wishes are within the permitted boundaries, then displays the result on the info-page (*127.0.0.1:1234/info*).
6. If the customers inputs are accepted a new .dfa-file is made with the relevant specs.
7. When the new .dfa-file is reloaded inside NX, the model will automatically be updated to the relevant specs. 

### Requirements ###

- Siemens NX (which has the programming language *Knowledge Fusion* imbedded, which was used for making .dfa-files used as templates for the chair)
- Python version 3.7
- Apache Jena Fuseki (SPARQL server)
- Olingvo (program for easily creating OWL-files which was uploaded to the Fuseki-server) or just Notebook for writing the OWL-files 

## Project 2 ##

This project task involved creating a KBE system for a scaffold-node-manufacturing company. The idea was to create a solution that allowed the customer to define different specifications of a node that would to be used to connect poles in scaffolds. The user needs to define what torque and force the node need to withstand, as well as the diameter of the poles that the node shall be attached to. The node would automatically be analyzed in Siemes NX by use of Nastran (FEM - multi-CAD finite element modeling), where the force and torque that the user defined would be inflicted in the holes of the 3D-mesh, and the deformation-simulation would then be shown to the user.

### Setup ###

Design the node-template in a .dfa-file. Initialize an apache web server, running locally on the computer.Run the DFAServerForNode.py-file which retrieves the input that the user submitted on the website and changes the diameter of the holes on the node. As we used journaling in NX (automatic creation of Python-code for every action within NX) to create the code used for analyzation, one has to go into NX and press "play" on the NXServer.py-file which starts the Analyzer.py-file. The Analyzer.py-file starts analyzing the node with the force and torque that was specified by the user. It also creates a GIF of the simulation (showing deformation on the node), and posts it to the info-website.

### User stories ###

The customer: 
1. The customer enters *127.0.0.1:1234/productConfig*. 
2. Then he/she enters the wanted force, torque and pipe-diameter for the node and presses the "submit"-button.
3. The customer then enters the info-page on *127.0.0.1:1234/info*. 
4. Here the customer can see the simulation-result of the node from NX. 

 #### GUI ####
 
The first image shows how the simple GUI for the customer-website looks like. The second shows how the info-website looks like (after the customer has ordered a node).

![alt text](https://github.com/thewildling/Knowledge_Based_Engineering/blob/main/Pictures/GUI-NodeInputs.png?raw=true)

![alt text](https://github.com/thewildling/Knowledge_Based_Engineering/blob/main/Pictures/GUI-NodeResults.png?raw=true)

### Sequence Diagram ###

![alt text](https://github.com/thewildling/Knowledge_Based_Engineering/blob/main/Pictures/Sequence%20diagram%20-%20Node.png?raw=true)

### Architecture ###

![alt text](https://github.com/thewildling/Knowledge_Based_Engineering/blob/main/Pictures/Architecture%20-%20Node.png?raw=true)

Walk through of the Architecture:

1. The product designer constructs a dfa-file to work as a template.
2. The customer enters the website under *127.0.0.1:1234/productConfig*, and is asked to put in the force/torque and diameter of the pipes. This is hosted by the DFA-server.
3. The DFA-server changes the parameter defining the node’s diameter and cutting radius of the removed parts, based on the diameter of the holes (or pipes) entered by the customer. 
4. The process engineer defines the boundary for the material to start deforming (290 Pascal on Aluminum in our case). 
5. The NX-server retrieves methods for analyzing the node from the Analyzer.py-file, and starts the analyzing by using Nastran (it has to be played off as a journal-file inside the NX-program).
6. The customer can enter the website *127.0.0.1:1234/info* to see the specifics of the node as well as an animation of the stress inflicted on the node. 


### Requirements ###

- Siemens NX (includes Nastran, which was used for analyzing the node)
- Python version 3.7
- Apache Jena Fuseki (SPARQL server)

## Project 3 ##

This project task involved creating a KBE system for a farmer. The idea is that the farmer needs a rail in the ceiling where a feeding-machine can run in order to feed animals. The solution is based on a predefined design of the rail, however the path of the rail is different based on the customer input. Since the rail is supposed to hang from the ceiling of a barn, it will look differently based on how the ceiling profile of the barn is, and most importantly where the animals are/where the feeder has to run through. This solution automatically creates a path between the feeding-spots, and also avoids any obstacles that the customer has defined (for example beams that are in the way). The customer could then see the result of how the rail would look like. 

### Setup ###

Design the rail-template in a .dfa-file. Initialize an apache web server, running locally on the computer. Run the App.py-file. 

### User stories ###

The customer: 
1. The customer enters the website *127.0.0.1:5000*.
2. Then he/she enters the rail-points, the obstacle-points and the height to the ceiling.
3. The customer can then see the resulting rail-path on the same website after a few seconds.

 #### GUI ####

The first image shows the startpage *127.0.0.1:5000*. We have focused on creating an intuitive user interface this time. The customer starts by entering the size of the room where the rail should be by filling in the grid-size and clicking “Generate room”. The customer can then click on the squares on the grid which either represents the coordinates in the room where the rail should be (in black) or where the obstacles should be (in red). The customer can then check the coordinates in the lists that show up on the left side, and edit the list if he/she wants to change the order or remove a point. If the customer clicks on the wrong squares he/she can also click the “Remove points”-button and click on them again to remove them.

![alt text](https://github.com/thewildling/Knowledge_Based_Engineering/blob/main/Pictures/GUI-RailInput.png?raw=true)

The box below pops up when the customer clicks on a rail-point. It asks the customer to enter the height to the ceiling for that point for which the beams (that holds up the rail) would be placed. 

![alt text](https://github.com/thewildling/Knowledge_Based_Engineering/blob/main/Pictures/GUI-RailHeights.png?raw=true)

When the customer has finished entering the input and clicked on the “Generate rail”-button the rail generated in NX will show up on the same website. It also shows the beams that hang from the ceiling to hold up the rail. This happens automatically. This way the customer does not have to do anything else than defining the inputs the first time. 

![alt text](https://github.com/thewildling/Knowledge_Based_Engineering/blob/main/Pictures/GUI-RailResult.png?raw=true)

### Sequence Diagram ###

![alt text](https://github.com/thewildling/Knowledge_Based_Engineering/blob/main/Pictures/Sequence%20diagram%20-%20Rail.png?raw=true)

### Architecture ###

![alt text](https://github.com/thewildling/Knowledge_Based_Engineering/blob/main/Pictures/Architecture%20-%20Rail.png?raw=true)

Walk through of the Architecture:

1. The product designer constructs a dfa-file to work as a template.
2. The customer enters the website under *127.0.0.1:5000*, and chooses the size of the room, the points where the rail should be, the points where there is an obstacle as well  as the height to the ceiling in the different points. This is hosted by App.py (which works as a “Main”-function for all the other ones).
3. The DFA-server retrieves the information from the user and runs the PathPlanner.py to plan the rail-path. 
4. The DFA-server then makes the necessary changes to the DFA-template.
5. NX then retrieves the KF-code from the DFA-file and creates the rail in NX.
6. The customer can then see the resulting rail on the user interface. 

### Requirements ###

- Siemens NX 
- Python version 3.7
- Apache Jena Fuseki (SPARQL server)

## Project 4 ##

In this project we have made a robotic arm, or more precisely; a 3-link open-chain manipulator. This manipulator works inside the environment of a sphere (in this case set to radius=100), but only the top-half because the robot-arm can not go beneath the ground. The length of each of the three links of the arm is determined by using Genetic Algorithm (search heuristic algortihm) in Python (GA.py-file). The algorithm generates a list of 3 lengths for each time it is run (can be done multiple times and give a large number of possible robot-arms). We have also made a script that creates the design of the arm by using OpenNX for Python (robot_arm.py-file).

### Setup / Requirements ###

- Python
- Siemens NX

One runs the python-file several times until it converges into the best solution.

### GUI ###

The picture below shows 5 different arms that has been generated by running robot_arm.py (which uses Ga.py for the lengths) 5 times. Here you can see that all of them are somewhat alike and reaches the given radius. We can therefore conclude that the genetic algorithm tries to find lengths that reaches as many points in the sphere as possible and can give multiple solutions. In robot_arm.py we have also tried to create the script in a manner so that the parameters (diameter of the 3 links and the joints) can be changed in the beginning of the script and will then change the design of the whole arm, which makes it easier to automate design modifications. 

![alt text](https://github.com/thewildling/Knowledge_Based_Engineering/blob/main/Pictures/Robotarm-Iterations.png?raw=true)

The picture below is the result after the robot arm had been rendered in NX to have a more real-like look to it. 

![alt text](https://github.com/thewildling/Knowledge_Based_Engineering/blob/main/Pictures/Robotarm-Rendered.png?raw=true)

