from field import Field
from helper import Helper

class StructField(Field):
    fields = []
    def __init__(self,conf):
        Field.__init__(self,conf)
        
        for fieldConf in conf['fields']:
            field = Helper.createField(fieldConf['type'],fieldConf)
            self.fields.append(field)
            
    def parseNode(self,node):
        result = {}
        for field in self.fields:
            result[field.name] = field.parse(node)
        return result

