from storage_MDP import *
import sys
import operator
class World_Grid_MDP(storage_MDP):
    def __init__(self, grid, terminals, init=(0, 0), gamma=.9):
        grid.reverse() ## because we want row 0 on bottom, not on top
        storage_MDP.__init__(self, init, actlist=orientations,terminals=terminals, gamma=gamma)
        update(self, grid=grid, rows=len(grid), cols=len(grid[0]))
        for x in range(self.cols):
            
            for y in range(self.rows):
                
                self.reward[x, y] = grid[y][x]
                #print y,x
                #print grid[y][x]
                if grid[y][x] == 1: 
                    self.reward[x,y] = -1
                if grid[y][x] == 3: 
                    self.reward[x,y] = -2
                if grid[y][x] == 4:
                    self.reward[x,y] = 1
                if x == (len(grid[0])-1):
                    if y == (len(grid)-1): 
                       self.reward[x,y] = 50
                if x == 0:
                    if y == 0:
                         self.reward[x, y] = 0
                if grid[y][x] != 2:
                    self.states.add((x,y))
     
    def transition_function(self, state, action):
        if action == None:
            return [(0.0, state)]
        else:
            return [(0.8, self.move(state, action)),
                    (0.1, self.move(state, turn_right(action))),
                    (0.1, self.move(state, turn_left(action)))]

    def move(self, state, direction):
        state1 = vector_add(state, direction)
        return if_(state1 in self.states, state1, state)
def iterate_MDP(mdp,ep):
    epsilon = ep
    U1 = dict([(s, 0) for s in mdp.states])
    reward_function, transition_function, gamma = mdp.reward_function, mdp.transition_function, mdp.gamma
    while True:
        U = U1.copy()
        delta = 0
        
        for s in mdp.states:
           
           
            U1[s] = float(reward_function(s)) + gamma * max([sum([p * U[s1] for (p, s1) in transition_function(s, a)])
                                        for a in mdp.movements(s)])
            delta = max(delta, abs(U1[s] - U[s]))
        if delta < epsilon * (1 - gamma) / gamma:
             return U
def best_policy(mdp, U):
    pi = {}
    for s in mdp.states:
        pi[s] = argmax(mdp.movements(s), lambda a:expected_utility(a, s, U, mdp))
    return pi
def expected_utility(a, s, U, mdp):
    return sum([p * U[s1] for (p, s1) in mdp.transition_function(s, a)])
def policy_iteration(mdp):
    U = dict([(s, 0) for s in mdp.states])
    pi = dict([(s, random.choice(mdp.movements(s))) for s in mdp.states])
    while True:
        U = policy_evaluation(pi, U, mdp)
        unchanged = True
        for s in mdp.states:
            a = argmax(mdp.movements(s), lambda a: expected_utility(a,s,U,mdp))
            if a != pi[s]:
                pi[s] = a
                unchanged = False
        if unchanged:
            return pi
def policy_evaluation(pi, U, mdp, k=20):
    reward_function, transition_function, gamma = mdp.reward_function, mdp.transition_function, mdp.gamma
    for i in range(k):
        for s in mdp.states:
            U[s] = reward_function(s) + gamma * sum([p * U[s] for (p, s1) in transition_function(s, pi[s])])
    return U
def print_path(the_Grid,ep):
    dic_of_utilities = iterate_MDP(the_Grid,ep)
    policy = best_policy(the_Grid,dic_of_utilities)
    x = 0
    y = 1 
    exit = False
    while exit != True:
        print x 
        print y 
        print exit
        if policy[x,y] == (0,1):
            print "Sqaure: ",x ,y
            print dic_of_utilities[x,y]
            y+=1
        if policy[x,y] == (1,0):
            print "Sqaure: ",x ,y
            print dic_of_utilities[x,y]
            x+=1
        if (y == len(the_Grid.grid)-1):
                print "The apples have been reached!"
                exit = True
    return