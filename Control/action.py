def getBlinds():
    i = True
    while i:
        bigBlind = input("Enter big blind: ")
        smallBlind = input("Enter small blind: ")
        blinds = [float(bigBlind), float(smallBlind)]
        if blinds[0] < blinds[1]:
            print("Error: Big blind smaller than Small Blind")
        else:
            i = False    
    print(blinds)
    return blinds

def getPlayerNumbers():
    numPlayers = input("Enter number of players: ")
    num = int(numPlayers)
    return num

def makeRoles(num):
    roleList = []
    for i in range(0,num):
        if i == 0:
            roleList.append("D") 
        elif i == 1:
            roleList.append("SB")
        elif i == 2:
            roleList.append("BB")
        elif i == 3:
            roleList.append("UTG")
        elif i == num-1: 
            roleList.append("C")
        elif i == num-2:
            roleList.append("HJ")
        elif i == num-3:
            roleList.append("LJ")
        else:
            roleList.append("UTG + " +  str(i-3))                                          
    print(roleList)
    return roleList

def makePlayers(num):
    needButton = True
    while needButton:
        playerNames = []
        playerList = []
        for i in range(1,num+1):
            playerList.append(i-1)
            playerNames.append(input("Enter name for P"+str(i)+": "))
            if needButton:
                button = input("Starting Dealer? (y/N): ")
                if button == "y":
                    needButton = False
                    print("P"+str(i)+" is the starting button")
                    buttonIndex = i-1
                if i == num and needButton:
                    print("No starting button found. Enter again")
    startingButton = playerNames[buttonIndex]    
    while startingButton != playerNames[num-1]:
        temp = playerNames.pop(0)
        playerNames.append(temp)

    print(playerNames)
    print(startingButton+" is the button")
    return playerNames

def playHand(blinds, numP, roleList):
    handAction = [[],[],[],[]]
    hand = [[],[],[],[]]

    foldedPlayers = []
    winner = False
    for i in range(0,4):
        match i:
            case 0:
                print("Pre-flop " + str(numP) + " ways")
            case 1:
                print("Flop " + str(numP-len(foldedPlayers)) + " ways")
            case 2:
                print("Turn " + str(numP-len(foldedPlayers)) + " ways")
            case 3:
                print("River " + str(numP-len(foldedPlayers)) + " ways")                
        if i == 0:
            hand[i].append(0)
            handAction[i].append(0)
            hand[i].append(blinds[1])
            handAction[i].append("sb")
            hand[i].append(blinds[0])
            handAction[i].append("bb")
            count = 3
            canCheck = False
            callAmount = blinds[0]
            limp = True
        else:
            hand[i].append(0)
            handAction[i].append(0)
            count = 1
            canCheck = True    
            callAmount = 0
            limp = False
        readyPlayers = len(foldedPlayers)
        a = True
        runningCount = count
        if count >= numP:
                count = 3%numP
        while a:
            print(foldedPlayers)
            for j in foldedPlayers:
                if j == roleList[count]:
                    hand[i].append("x")
                    handAction[i].append("x")
                    runningCount += 1
                    count += 1
                    if count == numP:
                        count = 0
                    continue    
            if len(foldedPlayers) == numP - 1:    
                print(roleList[count] + " wins")
                hand.append(roleList[count])
                winner = True
                break     
            inp = input("Enter " + roleList[count] + " action: ")
            if inp == "":
                if canCheck:
                    hand[i].append(0)
                    handAction[i].append(0) 
                    print(roleList[count] + " checks")
                    readyPlayers += 1
                else: 
                    foldedPlayers.append(roleList[count])
                    hand[i].append("x")
                    handAction[i].append("x")
                    readyPlayers += 1
                    print(roleList[count] + " folds") 
            elif inp == "c":
                if runningCount%numP == count and runningCount > count:
                    times = (runningCount-count)/numP
                    callDif = callAmount
                    for k in range(1,int(times)+1):
                        callDif -= (hand[i][-(k*numP)])
                    hand[i].append(callDif)
                else:    
                    hand[i].append(callAmount)
                handAction[i].append("c")    
                print(roleList[count] + " calls")
                readyPlayers += 1
            elif inp == "r":
                raiseAmount = input("Enter raise amount ($): ")
                if runningCount%numP == count and runningCount > count:
                    times = (runningCount-count)/numP
                    callDif = float(raiseAmount)
                    for k in range(1,int(times)+1):
                        callDif -= (hand[i][-(k*numP)])
                    hand[i].append(callDif)
                else:   
                    hand[i].append(float(raiseAmount))
                handAction[i].append("r") 
                limp = False   
                canCheck = False
                callAmount = float(raiseAmount)
                readyPlayers = 1 + len(foldedPlayers)
                print(roleList[count] + " raises to $" + str(raiseAmount))  
            else:
                print("Not a valid input")
                continue    
            runningCount += 1    
            count += 1
            if count == numP:
                count = 0
            if limp and count == 2:
                canCheck = True    
            if len(foldedPlayers) == numP - 1:    
                b = True
                while b:
                    c = False
                    for j in foldedPlayers:
                        if j == roleList[count]:
                            c = True
                    if c:
                        count += 1
                        if count == numP:
                            count = 0
                        continue
                    else:
                        b = False
                print(roleList[count] + " wins")
                hand.append(roleList[count])
                winner = True
                break     
            if readyPlayers == numP:
                a = False
        if winner:
            break        
        if i == 3:
            print("go to showdown")
            hand.append(input("Select winner: "))                    

    for i in range(0,len(hand)-1):
        if len(hand[i]) > 0:
            hand[i].pop(0)
            handAction[i].pop(0)

            
    roleIn = []
    for i in range(0,numP):
        roleIn.append([])       
    pot = 0        
    for i in range(0,len(hand)-1):
        for j in hand[i]:
            if j != 'x':
                pot += j
        for j in range(0,len(hand[i])):
            for k in range(0,numP):
                if j%numP == k:
                    roleIn[k].append(hand[i][j])

    roleInTotal = []               
    for i in range(0,numP):
        roleInTotal.append(0)
        for j in roleIn[i]:
            if j != 'x':
                roleInTotal[i] += j       

    temp = roleList.pop(0)
    roleList.append(temp)

    windex = 0
    for i in range(0,len(roleList)):
        if roleList[i] == hand[4]:
            windex = i

    return [hand, handAction, roleList, roleInTotal, roleIn, pot, windex]  

def printOverall(roleList, roleInTotal, pot, windex):
    print()
    print(roleList[windex] + " won $" + str(pot) + " GROSS and $" + str(pot-roleInTotal[windex]) + " NET")
    for i in range(0,len(roleList)):
        print(roleList[i] + " was in for $" + str(roleInTotal[i]))

def printPlayback(roleList, hand, handAction, numP, roleIn):
    print()
    for i in range(0,4):
        count = 0
        for j in range(0,len(hand[i])):
            print(roleList[count] + ": " + str(handAction[i][j]) + " - $" + str(hand[i][j]))
            count += 1
            if count == numP:
                count = 0
        print("------------------------------------------------")    
    print()
    for i in range(0,numP):
        print(roleList[i] + "- " + str(roleIn[i]))

 

def playGame(): 
    num = getPlayerNumbers()
    playerNames = makePlayers(num)
    blinds = getBlinds()
    
    theGameMustGoOn = True
    while theGameMustGoOn:
        
        roles = makeRoles(num)
        superList = playHand(blinds, num, roles)
        hand = superList[0]
        handAction = superList[1]
        roleList = superList[2]
        roleInTotal = superList[3]
        roleIn = superList[4]
        pot = superList[5]
        windex = superList[6]

        printOverall(playerNames, roleInTotal, pot, windex)
        printPlayback(roleList, hand, handAction, num, roleIn)

        temp = playerNames.pop(0)
        playerNames.append(temp)

        inp = input("Play another hand? (Y/n): ")
        if inp == "n":
            theGameMustGoOn = False



playGame()
