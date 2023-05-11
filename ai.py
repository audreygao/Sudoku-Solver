from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem) 

        assignment = {}
        stack = []
        while True:
            assignment, domains = self.propagate(assignment, domains)
            if (-1, -1) not in assignment:
                if len(assignment) == SD_SIZE ** 2:
                    return domains
                else:
                    assignment, x = self.make_decision(assignment, domains)
                    stack.append((copy.deepcopy(assignment), x, copy.deepcopy(domains)))
            else:
                if len(stack) == 0:
                    return None
                else:
                    assignment, domains = self.backtrack(stack)


    def propagate(self, assignment, domains):
        while True:
            # make assignment if domain becomes singleton
            for x in domains:
                if x not in assignment.keys() and len(domains[x]) == 1:
                    assignment[x] = domains[x]
            
            # domain reduction for spot that has been assigned a value       
            for x in assignment:
                if len(domains[x]) > 1:
                    domains[x] = [assignment[x]]
                    
            for x in domains:
                if len(domains[x]) == 0:
                    assignment[(-1, -1)] = -1
                    return assignment, domains
            
            
            consistency = True
            for x in domains:
                if len(domains[x]) == 1:
                    for y in sd_peers[x]:
                        value = domains[x][0] 
                        if value in domains[y]:
                            domains[y].remove(value)  #update domain according to constraint
                            consistency = False
            
            # return if there's no inconsistency in the whole grid
            if consistency == True:
                return assignment, domains
    
    def make_decision(self, assignment, domains):
        min_actions = 10
        spot = None
        for x in domains:
            if x not in assignment:
                if len(domains[x]) < min_actions:
                    min_actions = len(domains[x])
                    spot = x
        
        if spot is not None:
            value = random.choice(domains[spot])
            assignment[spot] = value
            return assignment, spot
    
    def backtrack(self, stack):
        assignment, x, domains = stack.pop()
        value = assignment[x]
        del assignment[x]
        domains[x].remove(value)
        return assignment, domains
