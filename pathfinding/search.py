import util

def manhattanHeuristic(state, problem):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = state
    xy2 = problem.goal_state
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def aStarSearch(problem):
    start = problem.getStartState()

    def cost(item):
        state=item[0]
        action=item[1][len(item[1])-1]
        return manhattanHeuristic(state, problem) + problem.getCostOfActions(item[1])
    
    queue=util.PriorityQueueWithFunction(cost)
    currItem=(start,[],[start])
    shortest_expansion = {start:manhattanHeuristic(start,problem)}
    while not problem.goalTest(currItem[0]):
        for action in problem.getActions(currItem[0]):
            newState = problem.getResult(currItem[0],action)
            newItem = (newState, currItem[1]+[action], currItem[2]+[newState]) 
            if newState in shortest_expansion:
                if cost(newItem) >= shortest_expansion[newState]:
                    continue
                elif cost(newItem) < shortest_expansion[newState]:
                    shortest_expansion[newState] = cost(newItem)
            else:
                shortest_expansion[newState] = cost(newItem)
            if newState not in currItem[2]:
                queue.push(newItem)
        if queue.isEmpty():
            return [start]
        currItem=queue.pop()
    return currItem[2]