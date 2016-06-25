
class ListField(Field):

    def parse(self,obj):
        if xpath != "":
            nodes = obj.xpath(xpath)
        else if cssPath != "":
            nodes = obj.css(xpath)
        else:
            return None

        result = []
        for node in nodes:
            result.append(self.parseNode(node))
        
        return result
    
    def parseNode(self,node):
        return self.getNodeText(node)

