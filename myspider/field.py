
class Field:
    name = None
    type = None
    xpath = None
    cssPath = None

    def parse(self,obj):
        if xpath != "":
            nodes = obj.xpath(xpath)
        else if cssPath != "":
            nodes = obj.css(xpath)
        else:
            return None

        if len(nodes) == 0:
            return None
        
        return None
    
    def parseNode(self,node):
        pass

    def getNodeText(self,node):
        nodes = node.childes

        text = ""
        for child in nodes:
            text += self.getNodeText(child)
        
        return text
