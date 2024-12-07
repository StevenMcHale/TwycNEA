class DynamicQueue(object):
    def __init__(self):
        self.__items = []
        self.__max = 150

    def enQueue(self, item):
        self.__items.append(item)

    def deQueue(self):
        temp = self.__items[0]
        del self.__items[0]
        return temp
    
    def isEmpty(self):
        if len(self.__items) == 0:
            return True
        else:
            return False
    
    def isFull(self):
        if len(self.__items) == self.__max:
            return True
        else:
            return False

    def showQueue(self):
        print(self.__items)

    def getQueue(self):
        return self.__items
    
    def getQueueLength(self):
        return len(self.__items)



class Stack(object):
    def __init__(self, pList):
        self.__stack = pList

    # push, pop, peek, isEmpty, isFull

    def push(self, item):
        self.__stack.append(item)

    def pop(self):
        temp = self.__stack[-1]
        del self.__stack[-1]
        return temp

    def peek(self):
        print(self.__stack[-1])

    def isEmpty(self):
        if len(self.__stack) == 0:
            return True
        else:
            return False

    def getStackLength(self):
        return len(self.__stack)
        


def bubbleSortBreaks(pList):

    for i in range(0, len(pList)-1):
        for j in range(0, len(pList) - i - 1):
            if pList[j]['Breaks'] < pList[j + 1]['Breaks']:
                temp = pList[j]
                pList[j] = pList[j + 1]
                pList[j + 1] = temp
    
    return pList


def bubbleSortDistance(pList):

    for i in range(0, len(pList)-1):
        for j in range(0, len(pList) - i - 1):
            if pList[j]['Distance'] > pList[j + 1]['Distance']:
                temp = pList[j]
                pList[j] = pList[j + 1]
                pList[j + 1] = temp
    
    return pList


def bubbleSortAlpha(pList):

    newList=[]

    # Remove Queryset

    for item in pList:
        newList.append(item)

    for i in range(0, len(newList)-1):
        for j in range(0, len(newList) - i - 1):
            if newList[j].name > newList[j + 1].name:
                temp = newList[j]
                newList[j] = newList[j + 1]
                newList[j + 1] = temp 
    
    return newList



def bubbleSortAlphaRooms(pList):

    newList=[]

    # Remove Queryset

    for item in pList:
        newList.append(item)

    for i in range(0, len(newList)-1):
        for j in range(0, len(newList) - i - 1):
            if newList[j].building.name > newList[j + 1].building.name:
                temp = newList[j]
                newList[j] = newList[j + 1]
                newList[j + 1] = temp
    
    return newList
