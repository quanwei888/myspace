
class TextField(Field):

    def parseNode(self,node):
        return self.getNodeText(node)
