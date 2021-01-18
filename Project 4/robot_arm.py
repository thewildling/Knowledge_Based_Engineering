#robot_arm.py
from shapes.Cylinder import Cylinder
import GA
import math

class make_robot:

    def generate_arms(self):
        myga = GA.MyGA(15, 30, 0.01, 5000) # sets the parameters for the algorithm
        #popsize, generations, mutationprob, radius of the sphere
        list = myga.main()
        l1 = list[0]
        l2 = list[1]
        l3 = list[2]
        armDiameter = 2
        angle1 = 70
        angle2 = 130

        
        vectorX1= math.sin(math.radians(angle1))
        vectorZ1=math.cos(math.radians(angle1))

        vectorX2= math.sin(math.radians(angle2))
        vectorZ2 = math.cos(math.radians(angle2))

        origin1x= math.sin(math.radians(angle1))*l2
        origin1y= math.cos(math.radians(angle1))*l2

        origin2x = math.sin(math.radians(angle2)) * l3
        origin2y = math.cos(math.radians(angle2)) * l3

        
        #making the base: 
        b1 = Cylinder(0, 0, 0, armDiameter * 2, 2, [0,0,1], "RED", "Wood")
        b1.initForNX()
        
        
        #arm one: 
        a1 = Cylinder(0, 0, 2, armDiameter, l1, [0,0,1], "RED", "Wood")
        a1.initForNX()
       
       
        #making the first joint:
        s1 = Cylinder(0, -armDiameter/2, armDiameter+l1, armDiameter * 2, armDiameter, [0,1,0], "RED", "Wood")
        s1.initForNX()
        
        #arm two: 
        a2 = Cylinder(0, 0, armDiameter+l1, armDiameter, l2, [vectorX1,0,vectorZ1], "RED", "Wood")
        a2.initForNX()

        #making the second joint
        s2 = Cylinder(origin1x, -armDiameter/2, armDiameter+l1 + origin1y, armDiameter * 2, armDiameter, [0,1,0], "RED", "Wood")

        s2.initForNX()
        
        #arm 3:
        a3 = Cylinder(origin1x, 0, armDiameter+l1+origin1y, armDiameter, l3, [vectorX2,0,vectorZ2], "RED", "Wood")
        a3.initForNX()

        # making the joint for the grabber
        s3 = Cylinder(origin1x + origin2x, -armDiameter/2, armDiameter+l1 + origin1y + origin2y, armDiameter, armDiameter, [0,1,0], "RED", "Wood")

        s3.initForNX()

        #grabber:
        g1 = Cylinder(origin1x + origin2x, -armDiameter/2, armDiameter+l1 + origin1y + origin2y, armDiameter / 2, armDiameter * 2, [vectorX2,-1,vectorZ2], "RED", "Wood")
        g2 = Cylinder(origin1x + origin2x, armDiameter/2, armDiameter+l1 + origin1y + origin2y, armDiameter / 2, armDiameter * 2, [vectorX2,1,vectorZ2], "RED", "Wood")
        g1.initForNX()
        g2.initForNX()


c1 = make_robot()
c1.generate_arms()