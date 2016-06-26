from field import Field

class TextField(Field):

    def parseNode(self,node):
        print self.getNodeText(node)
        return self.getNodeText(node)
