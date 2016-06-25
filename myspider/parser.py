
class Parser:
    fields = None

    def setFields(self,fields):
        self.fields = fields

    def parse(self,response):
        result = {}
        for field in self.fields:
            result[field.name] = field.parse(response)
            sefl.parseField(response,field)
        return result    
