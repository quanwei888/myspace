from list_field import ListField
from helper import Helper

class ListcompField(ListField):
    fields = []
    
    def __init__(self,conf):
        ListField.__init__(self,conf)
        
        for fieldConf in conf['fields']:
            field = Helper.createField(fieldConf['type'],fieldConf)
            self.fields.append(field)
           
    
    def parseNode(self,node):
        result = {}
        for field in self.fields:
            result[field.name] = field.parse(node)
        return result 

