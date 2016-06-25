
class CompField(Field):
    fields = None
    
    def parseNode(self,response,node):
        result = {}
        for field in fields:
            result[field.name] = field.parse(node)
        return result 

