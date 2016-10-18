#encoding=utf8

import sys
import numpy as np


'''
    text  :string
    idSeq:[(wordId,tagId)]
    valueSeq:[(word,tag)]
    lineSeq:[line,line]
'''

class TaggingUtil:
    WORD_NONE    =  "__NONE__"
    WORD_NONE_ID =  0  
    
    words =   {}
    tags       =   []
    word2Id    =   {}
    id2Word    =   {}
    tag2Id     =   {}
    id2Tag     =   {}
    
    #初始化
    def init(self,valueSeqList):
        valueSeq = []
        for seq in valueSeqList:
            valueSeq += [p for p in seq]
            
        words       =   [self.WORD_NONE]
        words       +=  list(set(w[0] for w in valueSeq))
        tags        =   []
        tags        +=  list(set(w[1] for w in valueSeq))
        
        #word to id
        word2Id     =   {}
        word2Id     =   dict((w,i+1) for i,w in enumerate(words))
        word2Id[self.WORD_NONE]   =   0
        id2Word     =   {}        
        id2Word     =   dict((v,k) for k,v in word2Id.items())
        
        #tag to id
        tag2Id     =   {}
        tag2Id     =   dict((w,i) for i,w in enumerate(tags))
        id2Tag     =   {}        
        id2Tag     =   dict((v,k) for k,v in tag2Id.items())


        self.words      =   words
        self.tags       =   tags
        self.word2Id    =   word2Id
        self.id2Word    =   id2Word
        self.tag2Id     =   tag2Id
        self.id2Tag     =   id2Tag
    
    #valueSeq->idSeq
    def valueSeqToIdSeq(self,valueSeq):
        idSeq = []
        
        for word in valueSeq:
            wordValue =   word[0]
            tagValue  =   word[1]
            wordId  =   (self.word2Id[wordValue] if self.word2Id.has_key(wordValue) else 0)
            tagId   =   (self.tag2Id[tagValue] if self.tag2Id.has_key(tagValue) else 0)
            idSeq.append((wordId,tagId))
        
        return idSeq
    
    #idSeq->valueSeq
    def idSeqTovalueSeq(self,idSeq):
        valueSeq = []
        
        for (wordId,tagId) in idSeq:
            wordValue =   self.id2Word[wordId]
            tagValue  =   self.id2Tag[tagId]
            valueSeq.append((wordValue,tagValue))
        
        return valueSeq
    
    #idSeq|valueSeq->skipSeq
    def seqToSkipSeq(self,mixSeq,maxSeqLen,leftPadding,rightPadding):
        skipSeq    =   []
        left = (maxSeqLen-1) / 2
        for i in range(0,len(mixSeq)):
            lpos = max(0,i-left)
            rpos = min(len(mixSeq),i-left+maxSeqLen)
            subSeq = mixSeq[lpos:rpos]
            if i-left < 0:
                subSeq = [leftPadding for k in range(i-left,lpos)] + subSeq
            if i-left+maxSeqLen >  len(mixSeq):
                subSeq = subSeq + [rightPadding for k in range(rpos,i-left+maxSeqLen)]
            skipSeq.append(subSeq)
        return skipSeq
    
    def valueSeqListToTrainData(self,valueSeqList,maxSeqLen):
        X = []
        Y = []
        trainSeq = []
        tagPos = (maxSeqLen-1) / 2
        for valueSeq in valueSeqList:
            idSeq  =   self.valueSeqToIdSeq(valueSeq)
            skipSeq =   self.seqToSkipSeq(idSeq, maxSeqLen, (0,0), (0,0))
            for seq in skipSeq:
                X.append([w[0] for w in seq])
                Y.append(self.idToArr(seq[tagPos][1],len(self.tags)))
        return (np.asarray(X),np.asarray(Y))
    
    def idToArr(self,id,arrLen):
        arr = np.zeros(arrLen)
        arr[id] = 1
        return arr
    
    def arrToId(self,arr):
        return int(np.argmax(arr))
    
    def trainDataToValueSeqList(self,trainData,maxSeqLen):
        (X,Y)   =   trainData
        tagPos = (maxSeqLen-1) / 2
        
        idSeq = []
        for i in range(0,len(X)):
            wordId  = X[i][tagPos]
            tagId   = self.arrToId(Y[i])
            idSeq.append((wordId,tagId))
        
        return self.idSeqTovalueSeq(idSeq)
    
    def trainDataToText(self,trainData,maxSeqLen):
        valueSeq =   self.trainDataToValueSeqList(trainData, maxSeqLen)
        return self.valueSeqToText(valueSeq)
        
    def textToTrainData(self,text,maxSeqLen):
        valueSeqList =   self.textToValueSeqList(text)
        if len(self.words) == 0:
            self.init(valueSeqList)
            
        trainData   =   self.valueSeqListToTrainData(valueSeqList, maxSeqLen)
        return trainData
    
    def textToValueSeqList(self,text):
        valueSeqList = []
        for lineSeq in text.split("\n"):
            valueSeq = []
            for seq in lineSeq.split(" "):
                if seq == "":
                    continue
                cols = seq.split("/")
                if len(cols) == 2:
                    word = cols[0]
                    tag  = cols[1]
                elif len(cols) == 1:
                    #表示是预测数据，不用关心tag的取值
                    word = cols[0]
                    tag  = None
                else:
                    continue
                valueSeq.append((word,tag))
            valueSeqList.append(valueSeq)
        return valueSeqList
    
    def valueSeqToText(self,valueSeq):
        return " ".join([w+"/" + t for (w,t) in valueSeq])

if __name__ == "__main__":
    text = u"#/w 地震/n 快讯/n #/u 中国/ns\n地震/n 台网/n 正式/ad 测定/v"
    print "--------text------"
    print text
    
    util    =   TaggingUtil()
    (X,Y) = util.textToTrainData(text,3)
    print "--------X------"
    print X
    print "--------Y------"
    print Y
    print "--------Text------"
    print util.trainDataToText((X,Y), 3)
    
    
    
