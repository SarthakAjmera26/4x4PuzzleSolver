#!/usr/bin/env python3
import time
from heapq import * # See heapq_test.py file to learn how to use. Visit : https://docs.python.org/3/library/heapq.html

def makeTuple(list_):
    return tuple(tuple(subList) for subList in list_)

def makeList(tuple_):
    return list(list(subTuple) for subTuple in tuple_)  

def initialise(initialState, goalState):
    initialStateTuple = makeTuple(initialState)
    goalStateTuple = makeTuple(goalState)

    goalCoordinates={}
    value={}
    for i in range(4):
        for j in range(4):
            goalCoordinates[goalState[i][j]]=(i,j)
            value[goalState[i][j]]=4*i+j

    return initialStateTuple, goalStateTuple, goalCoordinates, value

def getPosition(currentState,tile='0'):
    for i in range(4):
        for j in range(4):
            if(currentState[i][j]==tile):
                return i,j

def getNeighbours(currentState, posx, posy,dx,dy,actions):
    neighbours=[]
    for i in range(4):
        newx = posx + dx[i]
        newy = posy + dy[i]
        if(newx>=0 and newy>=0 and newx<4 and newy < 4):
            currentStateList = makeList(currentState)
            currentStateList[newx][newy], currentStateList[posx][posy] = currentStateList[posx][posy], currentStateList[newx][newy]
            newState = makeTuple(currentStateList)
            neighbours.append((newState,actions[i]))

    return neighbours
def heuristic(current, goalCoordinates,value):
    
    #manhattan
    MD=0
    for i in range(4):
        for j in range(4):
            tile = current[i][j]
            if(tile!='0'):
                x,y=goalCoordinates[tile]
                MD+=abs(i-x) + abs(j-y)

    #linear conflicts - horizontal
    for i in range(4):
        row=[]
        for j in range(4):
            tile = current[i][j]
            if(tile!='0'):
                x,y=goalCoordinates[tile]
                if(x==i):
                    row.append(value[tile])
        m = len(row)
        for j in range(m):
            for k in range(j+1,m):
                if(row[j]>row[k]):
                    MD+=2

    #linear conflicts - vertical
    for j in range(4): #col
        col=[]
        for i in range(4):
            tile = current[i][j]
            if(tile!='0'):
                x,y=goalCoordinates[tile]
                if(y==j):
                    col.append(value[tile])
        m = len(col)
        for j in range(m):
            for k in range(j+1,m):
                if(col[j]>col[k]):
                    MD+=2

        return MD



def A_Star(startState, goalState, goalCoordinates, value):
    heap = []
    cost = {}
    actions=['Up', 'Down','Left','Right']
    dx=[-1,1,0,0]
    dy=[0,0,-1,1]
    minPath=[]
    parent={}
    nodesGenerated=0

    heappush(heap,[heuristic(startState,goalCoordinates,value)+0,startState])
    cost[startState]=0
    parent[startState]=(None, None)

    while(len(heap)>0):
        #Should start node be included in nodesGenerated?
        currentState= heap[0][1]

        if(currentState==goalState):
            #print(cost[goalState])
            break
        heappop(heap)

        posX, posY = getPosition(currentState,'0')
        neighbours = getNeighbours(currentState, posX, posY,dx,dy,actions)

        for nextState,action in neighbours:
            nextStateCost = cost[currentState] + 1
            if nextState not in cost or nextStateCost<cost[nextState]:
                cost[nextState] = nextStateCost
                priority = nextStateCost + heuristic(nextState,goalCoordinates,value)
                heappush(heap,[priority,nextState])
                parent[nextState]=(currentState,action)

    cur = goalState
    while cur != startState:
        par,action=parent[cur] 
        minPath.append(action)
        cur = par

    nodesGenerated = len(cost)

    return minPath, nodesGenerated            


def FindMinimumPath(initialState,goalState):
    minPath=[] # This list should contain the sequence of actions in the optimal solution
    nodesGenerated=0 # This variable should contain the number of nodes that were generated while finding the optimal solution
    
    ### Your Code for FindMinimumPath function
    ### Write your program in an easy to read manner. You may use several classes and functions.
    ### Your function names should indicate what they are doing
    
    initialStateTuple, goalStateTuple, goalCoordinates, value = initialise(initialState, goalState)
    
    minPath, nodesGenerated = A_Star(initialStateTuple, goalStateTuple, goalCoordinates, value)

    return minPath, nodesGenerated
    ### Your Code ends here. minPath is a list that contains actions.
    ### For example, minPath = ['Up','Right','Down','Down','Left']
    

#**************   DO NOT CHANGE ANY CODE BELOW THIS LINE *****************************


def ReadInitialState():
    with open("initial_state2.txt", "r") as file: #IMP: If you change the file name, then there will be an error when
                                                        #               evaluators test your program. You will lose 2 marks.
        initialState = [[x for x in line.split()] for i,line in enumerate(file) if i<4]
    return initialState

def ShowState(state,heading=''):
    print(heading)
    for row in state:
        print(*row, sep = " ")

def main():
    initialState = ReadInitialState()
    ShowState(initialState,'Initial state:')
    goalState = [['0','1','2','3'],['4','5','6','7'],['8','9','A','B'],['C','D','E','F']]
    ShowState(goalState,'Goal state:')
    
    start = time.time()
    minimumPath, nodesGenerated = FindMinimumPath(initialState,goalState)
    timeTaken = time.time() - start
    
    if len(minimumPath)==0:
        minimumPath = ['Up','Right','Down','Down','Left']
        print('Example output:')
    else:
        print('Output:')

    print('   Minimum path cost : {0}'.format(len(minimumPath)))
    print('   Actions in minimum path : {0}'.format(minimumPath))
    print('   Nodes generated : {0}'.format(nodesGenerated))
    print('   Time taken : {0} s'.format(round(timeTaken,4)))

if __name__=='__main__':
    main()
