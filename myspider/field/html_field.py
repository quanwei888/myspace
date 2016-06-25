
class HtmlField(Field):

    def parseNode(self,node):
        return node.extract()
