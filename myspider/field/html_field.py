
from field import Field
class HtmlField(Field):

    def parseNode(self,node):
        return node.extract()
