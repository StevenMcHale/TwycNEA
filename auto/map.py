from main.models import *

class Node(object):
    def __init__(self, node):
        self.__node = node
        self.__links = {}
    
    def addlink(self, newNode, weight):
        self.__links[newNode] = weight

    def getNodeName(self):
        return self.__node
    
    def getLinks(self):
        return self.__links
    
    def getLinkWeight(self, nodeName):
        return self.__links[nodeName]



class Map(object):
    def __init__(self):
        self.__nodes = []
    
    def addNode(self, node):
        self.__nodes.append(node)

    def getNode(self, nodeName):
        for node in self.__nodes:
            if node.getNodeName() == nodeName:
                return node
    
    def getMap(self):
        return self.__nodes



buildings = Building.objects.all()

twyc_map = Map()

for building in buildings:
    newNode = Node(building.name)
    twyc_map.addNode(newNode)


for node in twyc_map.getMap():
    if node.getNodeName() == "KP":
        node.addlink("Berryfield", 7)
        node.addlink("Underwood", 3)
        node.addlink("Old Stables", 5)

    elif node.getNodeName() == "Old Stables":
        node.addlink("Berryfield", 2)
        node.addlink("KP", 5)
        node.addlink("Underwood", 8)

    elif node.getNodeName() == "Berryfield":
        node.addlink("Underwood", 10)
        node.addlink("KP", 7)
        node.addlink("Old Stables", 2)

    elif node.getNodeName() == "Underwood":
        node.addlink("Berryfield", 10)
        node.addlink("KP", 3)
        node.addlink("Old Stables", 8)



