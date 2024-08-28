from pyeda.inter import *

def edgeToBits(edge): # we covert the edge (27&3) to bits (~x1&~x2...)

    i, j = map(int, edge.split('&')) # first we split up the intgers from the &

    xBits = format(i, '05b')
    yBits = format(j, '05b') # convert both of them into bits

    xList = []
    for index, bit in enumerate(xBits): # iterate through the bits and depending on the bit we either add a ~ or not
        if bit == '0':
            xList.append('~x' + str(index + 1))
        elif bit == '1':
            xList.append('x' + str(index + 1))

    yList = []
    for index, bit in enumerate(yBits): # we also do it for the other number here
        if bit == '0':
            yList.append('~y' + str(index + 1))
        elif bit == '1':
            yList.append('y' + str(index + 1))

    xChangedBits = '&'.join(xList) # after we get the bits we join them together eith &
    yChangedBits = '&'.join(yList)

    return xChangedBits + '&' + yChangedBits # and return the combination of them

def change1(list): # use this function to just join them together with an &
    return "&".join(list)

def change2(list): # use this function to just join them together with an |
    return '|'.join(list)

def createExprList(EvenOrPrime, XorY):
    newList = []
    newList2 = []
    newList3 = []
    changeBit = XorY
    for num in EvenOrPrime: # loop through every num in the list and format it into bits
        bits = format(num, '05b')
        for i, bit in enumerate(bits): # loop through the bits
            if bit == '1': # if its a 1 then we dont add a ~
                changeBit = changeBit + str(i+1)
            elif bit == '0':# if its a 0 then we add the ~
                changeBit = '~'+ changeBit + str(i+1)
            newList.append(changeBit) # we then add it to the list
            changeBit = XorY # and reset changeBit
        newList2 = change1(newList) # we join it with an &
        newList3.append(newList2) # then add append to the last list
        newList = []
        newList2 = []
    return '|'.join(newList3) # then we join the final thing with |

def changeToExp(num1,num2): # we change the nums to an expr
    newList = []
    newList2 = []
    xBit = format(num1, '05b') # first we convert to bits
    xChangeBit = 'x'
    yChangeBit = 'y'
    yBit = format(num2, '05b') # first we convert to bits
    for i, bit in enumerate(xBit):
        if bit == '1': # if its a 1 then we dont add a ~
            xChangeBit = xChangeBit + str(i+1)
        elif bit == '0': # if its a 0 then we add the ~
            xChangeBit = '~'+ xChangeBit + str(i+1)
        newList.append(xChangeBit) # then we append the new item to the list
        xChangeBit = 'x'
    combineX = ", ".join(newList) # then we join it with a ,
    for i, bit in enumerate(yBit):
        if bit == '1': # if its a 1 then we dont add a ~
            yChangeBit = yChangeBit + str(i+1)
        elif bit == '0': # if its a 0 then we add the ~
            yChangeBit = '~'+ yChangeBit + str(i+1)
        newList2.append(yChangeBit) # then we append the new item to the list
        yChangeBit = 'y'
    combineY = ", ".join(newList2) # then we join it with a , 
    return "And(" + combineX + ", " + combineY + ")" # and return it with And with () around it

def changeSingleToExp(num1,YorX): # we change a single num to an expr
    newList = []
    Bit = format(num1, '05b') # first we convert to bits
    changeBit = YorX
    for i, bit in enumerate(Bit): # we iterate through the bits
        if bit == '1': # if its a 1 then we dont add a ~
            changeBit = changeBit + str(i+1)
        elif bit == '0': # if its a 0 then we add the ~
            changeBit = '~'+ changeBit + str(i+1)
        newList.append(changeBit) # then we append the new item to the list
        changeBit = YorX # reset the changeBit
    Combined = ", ".join(newList) # then we join it with a , 
    return "And(" + Combined + ")" # and return it with And with () around it

def testRRBDD(BDD, num1, num2): # to test the RR bdd we just get two number adn make them into the expr 
    find = changeToExp(num1,num2) # after we make the expr then we search for in the BDD
    expr = bdd2expr(BDD)

    if find in str(expr): # if we find it in the BDD then we return true
        return True
    else:
        return False

def testEvenBDD(BDD, num): # to test the Even BDD we just check the LSB of the number and if its a 0 then we know that its in the BDD
    find = changeSingleToExp(num,'x')
    expr = bdd2expr(BDD)
    if "~x5" in find:
        find = "~x5"
        if find in str(expr):
            return True
        else:
            return False
    else:
        return False

def testPrimeBDD(BDD, num): # to test Prime we check if the expr of that number is in the primeBDD
    find = changeSingleToExp(num, 'y') # the full expr
    find2 = find.replace(', y4', '') # expr without the 4th bit
    expr = bdd2expr(BDD)

    if find in str(expr) or find2 in str(expr): # and check if its in the expr of prime BDD
        return True
    else:
        return False

def testStatementA(even, prime, RR): # we test the statementA given from the pdf 
    i = 0
    for u in range(0, 32):
        for v in range(0, 32): # we loop through the u and v for 32
            if testPrimeBDD(prime, u) == 1: # and if its a prime number then we move on to even and in RR
                result = testEvenBDD(even, v) & testRRBDD(RR, u, v) 
                if result == False & v == 31:
                    return False
    return True
    
def void_main():
    varX = [bddvar("x1"), bddvar("x2"), bddvar("x3"), bddvar("x4"), bddvar("x5")]

    varY = [bddvar("y1"), bddvar("y2"), bddvar("y3"), bddvar("y4"), bddvar("y5")]

    varZ = [bddvar("z1"), bddvar("z2"), bddvar("z3"), bddvar("z4"), bddvar("z5")] # made a list for each bdd variable for x,y,and z

    RList = [] # we loop through 32 for each i and j for the nodes and if it fits the RR conditon then we append it to the R list in the format (27&3)
    for i in range(0, 32):
        for j in range(0, 32):
            if (i + 3) % 32 == j % 32 or (i + 8) % 32 == j % 32:
                edge = str(i) + '&' + str(j)
                RList.append(edge) 
    R = [] # after we get it into the format (27&3) then we make each into its bits with x and y example for 1 -> (~x1&~x2&~x3&~x4&x5)
    for edge in RList:
        newEdge = edgeToBits(edge)
        R.append(newEdge)
    R = change2(R) # we join the each bit with a | 
    evenList = [] # populate the evenList with each even number
    for i in range(0,32):
        if i % 2 == 0:
            evenList.append(i)
    primeList = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31] # prime number list

    prime = createExprList(primeList, 'y') # then we put both prime and the even into a function to make them a expr for each number
    even = createExprList(evenList, 'x')
    RR = expr2bdd(expr(R)) # then we make the R into RR by making a an expr 2 a bdd

    primeBDD = expr2bdd(expr(prime))
    evenBDD = expr2bdd(expr(even))

    # we make RR2 in one line by using compose with RR and smoothing out the Zs
    RR2 = (RR.compose({varX[0]: varZ[0], varX[1]: varZ[1], varX[2]: varZ[2], varX[3]: varZ[3], varX[4]: varZ[4]}) & RR.compose({varY[0]: varZ[0], varY[1]: varZ[1], varY[2]: varZ[2], varY[3]: varZ[3], varY[4]: varZ[4]})).smoothing(varZ)
    tempBDD = RR2
    tempBDD2 = None
    while True: # algorithm to make RR2 into RRstar
        tempBDD2 = tempBDD
        tempBDD = (tempBDD.compose({varX[0]: varZ[0], varX[1]: varZ[1], varX[2]: varZ[2], varX[3]: varZ[3], varX[4]: varZ[4]}) & tempBDD.compose({varY[0]: varZ[0], varY[1]: varZ[1], varY[2]: varZ[2], varY[3]: varZ[3], varY[4]: varZ[4]})).smoothing(varZ) | tempBDD2
        if tempBDD.equivalent(tempBDD2):
            break
    
    RR2star = tempBDD

    print("Test for RR(27,3) = " + str(testRRBDD(RR, 27, 3)) + " ----- Expected: True") # all the test cases for each one given in the pdf
    print("Test for RR(27,3) = " + str(testRRBDD(RR, 16, 20)) + " ----- Expected: False")
    print("Test for EVEN(14) = " + str(testEvenBDD(evenBDD, 14)) + " ----- Expected: True")
    print("Test for EVEN(13) = " + str(testEvenBDD(evenBDD, 13)) + " ----- Expected: False")
    print("Test for PRIME(7) = " + str(testPrimeBDD(primeBDD, 7)) + " ----- Expected: True")
    print("Test for PRIME(2) = " + str(testPrimeBDD(primeBDD, 2)) + " ----- Expected: False")
    print("Test for RR(27,6) = " + str(testRRBDD(RR2, 27, 6)) + " ----- Expected: True")
    print("Test for RR(27,9) = " + str(testRRBDD(RR2, 27, 9)) + " ----- Expected: False") 
    print("Test for StatementA = " + str(testStatementA(evenBDD, primeBDD, RR2star)) + " ----- Expected: True")

if __name__ == '__main__':
    void_main()