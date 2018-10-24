'''
A multi-floor building has a Lift in it.

People are queued on different floors waiting for the Lift.

Some people want to go up. Some people want to go down.

The floor they want to go to is represented by a number (i.e. when they enter the Lift this is the button they will
press)

BEFORE (people waiting in queues)               AFTER (people at their destinations)
                   +--+                                          +--+
  /----------------|  |----------------\        /----------------|  |----------------\
10|                |  | 1,4,3,2        |      10|             10 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 9|                |  | 1,10,2         |       9|                |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 8|                |  |                |       8|                |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 7|                |  | 3,6,4,5,6      |       7|                |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 6|                |  |                |       6|          6,6,6 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 5|                |  |                |       5|            5,5 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 4|                |  | 0,0,0          |       4|          4,4,4 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 3|                |  |                |       3|            3,3 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 2|                |  | 4              |       2|          2,2,2 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 1|                |  | 6,5,2          |       1|            1,1 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 G|                |  |                |       G|          0,0,0 |  |                |
  |====================================|        |====================================|
Rules
Lift Rules
The Lift only goes up or down!
Each floor has both UP and DOWN Lift-call buttons (except top and ground floors which have only DOWN and UP
respectively)
The Lift never changes direction until there are no more people wanting to get on/off in the direction it is already
travelling
When empty the Lift tries to be smart. For example,
If it was going up then it may continue up to collect the highest floor person wanting to go down
If it was going down then it may continue down to collect the lowest floor person wanting to go up
The Lift has a maximum capacity of people
When called, the Lift will stop at a floor even if it is full, although unless somebody gets off nobody else can get on!
If the lift is empty, and no people are waiting, then it will return to the ground floor
People Rules
People are in "queues" that represent their order of arrival to wait for the Lift
All people can press the UP/DOWN Lift-call buttons
Only people going the same direction as the Lift may enter it, and they do so according to their "queue" order
If a person is unable to enter a full Lift, they will press the UP/DOWN Lift-call button again after it has departed
without them
Kata Task
Get all the people to the floors they want to go to while obeying the Lift rules and the People rules
Return a list of all floors that the Lift stopped at (in the order visited!)
NOTE: The Lift always starts on the ground floor (and people waiting on the ground floor may enter immediately)

I/O
Input
queues a list of queues of people for all floors of the building.
The height of the building varies
0 = the ground floor
Not all floors have queues
Queue index [0] is the "head" of the queue
Numbers indicate which floor the person wants go to
capacity maximum number of people allowed in the lift
Parameter validation - All input parameters can be assumed OK. No need to check for things like:

People wanting to go to floors that do not exist
People wanting to take the Lift to the floor they are already on
Buildings with < 2 floors
Basements
Output
A list of all floors that the Lift stopped at (in the order visited!)
'''




class Dinglemouse(object):
    def __init__(self, queues, capacity):
        self.queues=[]
        self.capacity=capacity
        self.elevatorContents =[]
        self.currentFloor=0
        self.rising = True
        self.floorsStoppedAt=[0]
        self.passangersToDropOff =0
        ##create new 2d array of Lists instead of tuples.
        for index in range(len(queues)):
            ##calculate number of passangers to drop off
            self.passangersToDropOff += len(queues[index])
            ##recreate as 2d list
            newList=[]
            for index2 in range(len(queues[index])):
                newList.append(queues[index][index2])
            self.queues.append(newList)

    def changeFloors(self):
        """Changes the elevators floor by the direction it's headed in"""
        if self.rising:
            self.currentFloor+=1
        else:
            self.currentFloor-=1
    def checkTopOrBottomFloors(self):
        """Changes elevator direction when it reaches top or bottom floors"""
        if self.currentFloor==0:
            self.rising=True
        if self.currentFloor==len(self.queues)-1:
            self.rising=False

    def checkIfLiftStopped(self):
        """Checks whether the lift stops at a particular floor and if so, handles the functionality for
        passengers getting on and off."""
        liftStopped = False
        # Check who gets off
        for num in reversed(range(len(self.elevatorContents))):
            if self.elevatorContents[num]==self.currentFloor:
                self.elevatorContents.pop(num)
                #remove person needed to drop off from loop
                self.passangersToDropOff-=1
                liftStopped=True
        peopleWhoBoarded=[]
        #Check who gets on.
        for personPos in range(len(self.queues[self.currentFloor])):
            #Here we double check the lift is going the right way
            isRightWay = self.isGoingRightWay(self.queues[self.currentFloor][personPos])
            if isRightWay==True:
                liftStopped = True
                if len(self.elevatorContents) < self.capacity:
                    self.elevatorContents.append(self.queues[self.currentFloor][personPos])
                    peopleWhoBoarded.append(personPos)
        #remove boarders from main list by iterating over list of index in reverse and removing them.
        for index in reversed(peopleWhoBoarded):
            self.queues[self.currentFloor].pop(index)
        if liftStopped:
            #Check its not the same floor twice(so no double count of top and bottom floors)
            if self.floorsStoppedAt[len(self.floorsStoppedAt)-1]!=self.currentFloor:
                self.floorsStoppedAt.append(self.currentFloor)
                self.liftTakeOff=False

    def doesElevatorTurn(self):
        """If there is nobody wanting a floor in the direction the elevator is headed, this method changes
        the elevator's direction."""
        if len(self.elevatorContents)>0:
            if self.rising:
                if self.currentFloor>=max(self.elevatorContents):
                    self.rising=False
            else:
                if self.currentFloor<=min(self.elevatorContents):
                    self.rising=True
    def theLift(self):
        """Main functionality of the lift class"""
        while self.passangersToDropOff>0:
            self.checkTopOrBottomFloors()
            self.checkIfLiftStopped()
            self.doesElevatorTurn()
            self.changeFloors()
        if len(self.floorsStoppedAt)>0:
            if self.floorsStoppedAt[len(self.floorsStoppedAt)-1]!=0:
                self.floorsStoppedAt.append(0)
        return self.floorsStoppedAt

    def isGoingRightWay(self, desiredFloor):
        """Checks the Lift is going in the direction the passanger wants"""
        if desiredFloor>self.currentFloor:
            if self.rising:
                return True
        if desiredFloor<self.currentFloor:
            if self.rising==False:
                return True
        return False


if __name__ == "__main__":
    tests = [[ ( (),   (),    (5,5,5), (),   (),    (),    () ),     [0, 2, 5, 0]          ],
             [ ( (),   (),    (1,1),   (),   (),    (),    () ),     [0, 2, 1, 0]          ],
             [ ( (),   (3,),  (4,),    (),   (5,),  (),    () ),     [0, 1, 2, 3, 4, 5, 0] ],
             [ ( (),   (0,),  (),      (),   (2,),  (3,),  () ),     [0, 5, 4, 3, 2, 1, 0] ]]
    for queues, answer in tests:
        print("=== Running test for data: [{}]".format(queues))
        lift = Dinglemouse(queues, 5)
        result =lift.theLift()
        if result == answer:
            print("=== CORRECT: Largest Island Size = {}\n\n".format(answer))
        else:
            print("=== FAIL: Size should be {} result was {}".format(answer, result))

