# Knowledge_Based_Engineering
This repository includes all projects completed by my team during the course *TMM4275 Knowledge-base Engineering* at NTNU.

## Project 1 ##

This project task involved creating a KBE system for a chair-manufacturing company. The idea was to create a solution that allowed the customer to define different specifications of the chair (height, lenght of feet, thickness, color etc.), and then present the finished design to the user without the user needing any engineering/programming skills. The solution would design the chair in Siemes NX automatically based on only a few parameters from the customer input. This solution was created for 2 specific users: the customer and the process engineer. The reason for creating a UI for the process engineer as well was that the factory would have limits on their equipment, and thereby limits on the chairs that could be made.

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

### Architecture ###

Walk through of the Architecture:

1. The product designer constructs a .dfa-file to work as a template.
2. The process engineer enters the website *127.0.0.1:4321/process*, and sets the constraints for the design space (machinery). This is hosted by the Manufacturing request server.
3. The constraints are sent via the Manufacturing request server to a Apache Jenna Fuseki server online, where a query is used to insert them in the correct place in the OWL file. 
4. The customer then enters the website under *127.0.0.1:1234/productConfig*, and is asked to put in the measurements of the desired product. This is hosted by the DFA-server.
5. The DFA-server connects to the fuseki-server and sends a query to retrieve the max/min constraints. The DFA-server checks if the customer's wishes are within the permitted boundaries, then displays the result on the info-page (*127.0.0.1:1234/info*).
6. If the customers inputs are accepted a new .dfa-file is made with the relevant specs.
7. When the new .dfa-file is reloaded inside NX, the model will automatically be updated to the relevant specs. 


