import random

class MyGA:
    
    def __init__(self, populationsize, generations, mutation_problem, radius_of_sphere):
        self.populationsize = populationsize
        self.generations = generations
        self.mutProb = mutation_problem
        self.radius = radius_of_sphere #radius of outer sphere 
        
        self.datapoints = [] #placeholderlist for the data of armlengths
        for i in range(0, self.populationsize):
            arm = []
            for part in range(0,3):
                arm.append(random.randint(1,31)) 
            self.datapoints.append(arm) 
        self.currGeneration = self.datapoints

    def crossover(self, parent_one, parent_two):
        # makes a function that deals with the crossovers. We set it to 28(11100) and 3(00011)
        mask_head = 28
        mask_tail = 3
        child_one = []
        child_two = []
        for i in range(0,3):
            child_one.append((parent_one[i] & mask_head) + (parent_two[i] & mask_tail)) # head of parent 1, tail of parent 2
            child_two.append((parent_two[i] & mask_head) + (parent_one[i] & mask_tail)) # head of parent 2, tail of parent 1
        return child_one, child_two
        

    def fitness(self, individual, currGeneration):
        # this function is made so that it will calc. the score of each pop, so we can select the most capable.
        # first we want to minimize (rad1 + rad2 - big_rad)^2. We do this so that we are able to reach the whole radius.
        # secondly we will try to minimize (radfirst - big_rad)^2. This id done to make the arm not reach groundlevel.
        # third we minimize (rad1 - rad2)^2. As we discused in class, this is so we can reach as many points as possible in the sphere.
        # Those close to the arms center as well.
        # Last we check the sums of the above-mentioned criteria
        score = 1 / (5 * (individual[1] + individual[2] - self.radius) ** 2 + 2 * (self.radius - individual[0]) ** 2 + 2 * (individual[1] - individual[2]) ** 2 + 0.2)
        sum_of_criteria = 0
        for x in range(0, len(currGeneration)):
            sum_of_criteria += 1 / (5 * (currGeneration[x][1] + currGeneration[x][2] - self.radius) ** 2 + 2 * (self.radius - currGeneration[x][0]) ** 2 + 2 * (currGeneration[x][1] - currGeneration[x][2]) ** 2 + 0.2)
        return score / sum_of_criteria
        
    def selection(self, currGeneration):
        #this is a solution to our problem, and has been discussed in the lectures.

        selectionprobs = []
        current_prob = 0
        for element in range(0, self.populationsize):
            #here we create the probability for the pop. This is determined by the fitness function.
            current_prob += self.fitness(currGeneration[element], currGeneration)
            selectionprobs.append(current_prob)
        
        new_population = currGeneration.copy()
        for i in range(0, self.populationsize):
            r = random.random()
            selected = 0
            while r > selectionprobs[selected]:
                selected +=1
            new_population[i] = currGeneration[selected]	#generates an individual for the new pop.

        return new_population

    def mutate(self, population):
        # this is a version of a mutation-function. we use it ti check if a mutation will occur.
        probNoMut = (1-self.mutProb)**(self.populationsize * 5 * 3)
        #checks if 1-bit muation has occured.
        check = random.random()
        #a while loop to see if a mutationprecent is higher than probability of no mutation.
        while check > probNoMut:
            check = check - probNoMut
            #selects a individual from the pop.
            theIndividual = random.randrange(0, self.populationsize, 1)
            part = random.randrange(0,3)
            theBit = random.randrange(0, 5, 1) 
            ind = population[theIndividual]
            indpart = ind[part]
            #transforms to the right amount of bits
            bin_ind = format(indpart, '#07b')
            #access the right bit 
            digit = bin_ind[theBit +2]
            #represent the binary number as a list of characters 
            listbi = list(bin_ind)

            if digit == '0':
                #turn 0 to 1
                listbi[theBit +2] ='1'
            else: 
                #turn 1 to 0
                listbi[theBit +2] ='0'
            #transform to dec
            bin_mut = ''.join(listbi)
            mutpart = int(bin_mut[2:], 2)
            mutated = ind
            mutated[part] = mutpart

            #check if mutated is better fitted than previous.
            fitNew = self.fitness(mutated, population)
            fitCurr = self.fitness(ind, population)
            if(fitNew > fitCurr):
                population[theIndividual] = mutated

        return
    
    def main(self):
        # the main method for running the GA. what we call in robot_arm to generate the list of lengths.
        nextGeneration = self.datapoints
        #for loop to iterate trough the gen.
        for gen in range(1, self.generations):
            currGeneration = nextGeneration.copy()
            nextGeneration.clear()
            
            # Select the fittest parents for crossover
            selection = self.selection(currGeneration)
            nextGeneration = selection.copy()
            # we use the crossover-function on 1/3 of the pop.
            for gen in range(0, (self.populationsize) // 6, 2):
                child_one, child_two = self.crossover(selection[gen],selection[gen+1]) #use two parents to make 2 children, using the crossover-function.
                nextGeneration[gen] = child_one # adding the children to the next generation
                nextGeneration[gen + 1] = child_two
            
            # check on self before looping on.
            self.mutate(nextGeneration)
        
        #this gives us the best of the generation.
        Results_of_fitness = []
        for individual in nextGeneration:
            Results_of_fitness.append(self.fitness(individual, nextGeneration))
        return nextGeneration[Results_of_fitness.index(max(Results_of_fitness))]


