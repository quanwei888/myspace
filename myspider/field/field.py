
class Field:
    name = ""
    type = "text"
    xpath = None
    cssPath = None
    
    def __init__(self,conf):
        self.name = conf['name']
        self.type = conf['type']
        self.xpath = conf.get("xpath","")
        self.cssPath = conf.get("cssPath","")

    def parse(self,obj):
        if self.xpath != "":
            nodes = obj.xpath(self.xpath)
        elif self.cssPath != "":
            nodes = obj.css(self.cssPath)
        else:
            return None
        
        if len(nodes) == 0:
            return None
        return self.parseNode(nodes[0])
    
    def parseNode(self,node):
        pass

    def getNodeText(self,node):
        nodes = node.xpath("./node()")

        text = ""
        if len(nodes) == 0:
            text = node.extract()
        else:
            for child in nodes:
                text += self.getNodeText(child)
        
        return text
