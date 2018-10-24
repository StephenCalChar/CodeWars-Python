'''A group of N golfers wants to play in groups of G players for D days in such a way that no golfer plays more than
once with any other golfer. For example, for N=20, G=4, D=5, the solution at Wolfram MathWorld is

Write a function that validates a proposed solution, a list of list of strings, as being a solution to the social
golfer problem. Each character represents a golfer, and each string is a group of players. Rows represent days.
The solution above would be encoded as:
You need to make sure (1) that each golfer plays exactly once every day, (2) that the number and size of the groups is
 the same every day, and (3) that each player plays with every other player at most once.

So although each player must play every day, there can be particular pairs of players that never play together.

It is not necessary to consider the case where the number of golfers is zero; no tests will check for that. If you do
wish to consider that case, note that you should accept as valid all possible solutions for zero golfers, who
(vacuously) can indeed play in an unlimited number of groups of zero.
'''

def valid(a):
    isValidSchedule =True
    #Create Dictionary.
    golferSchedule ={}
    #Creates a dictionary with Golfer as Key and golfers playued with as value.
    for day in a[0]:
        for player in day:
            if player in golferSchedule:
                return False
            else:
                golferSchedule[player]=[]

    #1.that each golfer plays exactly once every day,
    #this is calculated within a combination of 1 and 2.
    #2.that the number and size of the groups is the same every day.
    numberOfGroups=[]
    groupSize=[]
    for day in a:
        groupSize.append(len(day))
        for group in day:
            numberOfGroups.append(len(group))

    if len(set(groupSize))!=1:
        return False
    if len(set(numberOfGroups))!=1:
        return False

    #3. that each player plays with every other player at most once.
    for day in a:
        for group in day:
            for player in range(len(group)):
                for opponent in range(len(group)):
                    if player!=opponent:
                        # If opponent is in dictionary list return false as they have already played.
                        if group[opponent] not in golferSchedule.keys():
                            return False
                        if group[opponent] in golferSchedule[group[player]]:
                            return False
                        #ELse if opponent is not in dictionary list already appened it.
                        golferSchedule[group[player]].append(group[opponent])
    return isValidSchedule




a = [
    ['ABCD', 'EFGH', 'IJKL', 'MNOP', 'QRST'],
    ['AEIM', 'BJOQ', 'CHNT', 'DGLS', 'FKPR'],
    ['AGKO', 'BIPT', 'CFMS', 'DHJR', 'ELNQ'],
    ['AHLP', 'BKNS', 'CEOR', 'DFIQ', 'GJMT'],
    ['AFJN', 'BLMR', 'CGPQ', 'DEKT', 'HIOS']]

b= [
    ["AB", "CD"],
    ["AD", "BC"],
    ["BD", "AC"]]


c = [
    ["AB", "CD", "EF", "GH"],
    ["AC", "BD", "EG", "FH"],
    ["AD", "CE"],
    ["AE", "BG", "CH", "FD"]]

d = [
    ["ABC", "DEF"],
    ["ADE", "CBF"]]

if __name__ == "__main__":
    # Run tests
    testData = [
        (a, True),
        (b, True),
        (c, False),
        (d, False)
        ]
    counter =1
    for inputData, expectedResult in testData:
        print("=== Running test for data: [{}]".format(counter))
        result = valid(inputData)
        if result == expectedResult:
            print("=== CORRECT: Largest Island Size = {}\n\n".format(result))
        else:
            print("=== FAIL: Size should be {} result was {}".format(expectedResult, result))
        counter += 1

