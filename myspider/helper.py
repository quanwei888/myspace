
import importlib
import re

class Helper:
    @staticmethod
    def getParsersByUrl(parsers,url):
        results = []
        for parser in parsers:
            if Helper.canMatch(parser.url, url):
                results.append(parser)
                #print "parser:" + url
        return results
    
    @staticmethod
    def getRulesByUrl(rules,url):
        results = []
        for rule in rules:
            if Helper.canMatch(rule.fromUrl, url):
                results.append(rule)
                #print "rule:" + url
        return results
    
    @staticmethod
    def canMatch(pattern,text):
        return re.match(pattern,text) != None

    @staticmethod
    def createExtractor(name):
        clsName = name.capitalize() + "Extractor"
        moduleName = "extractor." + name + "_extractor"
        
        moduleObj = importlib.import_module(moduleName)
        classObj = getattr(moduleObj, clsName)
        
        return classObj()
        
    @staticmethod
    def createField(name,conf):
        clsName = name.capitalize() + "Field"
        moduleName = "field." + name + "_field"
        
        moduleObj = importlib.import_module(moduleName)
        classObj = getattr(moduleObj, clsName)
        
        return classObj(conf)

