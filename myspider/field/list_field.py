from field import Field
class ListField(Field):

    def parse(self,obj):
        if self.xpath != "":
            nodes = obj.xpath(self.xpath)
        elif self.cssPath != "":
            nodes = obj.css(self.cssPath)
        else:
            return None

        result = []
        for node in nodes:
            result.append(self.parseNode(node))
        
        return result
    
    def parseNode(self,node):
        return self.getNodeText(node)

