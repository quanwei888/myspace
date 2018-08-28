# encoding=utf8
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from torch.utils.data import Dataset, DataLoader

class SimLSTMModel(nn.Module):
    def __init__(self, vocabSize, emdDim, encDim):
        super(SimLSTMModel, self).__init__()
        self.vocabSize = vocabSize
        self.emdDim = emdDim
        self.encDim = encDim
        
        self.emb = nn.Embedding(vocabSize, emdDim)
        self.lstm = nn.LSTM(emdDim, encDim)
        self.fc = nn.Linear(encDim * 4, 2)

    def forward(self, inputs):
        query, title = inputs
         
        queryEmb = self.emb(query)
        queryEmb = torch.transpose(queryEmb,0,1)
        out, hiden = self.lstm(queryEmb)
        queryEnc = out[-1]
        
        titleEmb = self.emb(title)
        titleEmb = torch.transpose(titleEmb,0,1)
        out, hiden = self.lstm(titleEmb)
        titleEnc = out[-1]
        
        mulEnc = queryEnc * titleEnc
        addEnc = queryEnc + titleEnc
        catEnc = torch.cat([queryEnc, titleEnc, mulEnc, addEnc], 1) 
        
        out = self.fc(catEnc)
        return out

class SimDataset(Dataset):
    def __init__(self, trainFile, vocFile, queryLen, docLen,negSample=0,maxSample=1000000000000):
        self.queryLen = queryLen 
        self.docLen = docLen 
        self.maxSample = maxSample
        self._UN_ = 0
        self._PAD_ = 1
        
        self.word2id = self.loadVoc(vocFile)
        self.data = self.loadData(trainFile)
        if negSample>0:
            self.genNegtiveSample(negSample)
    
    def loadVoc(self,vocFile):
        word2idFile = open(vocFile, "r")
        word2id = {}
        for text in word2idFile:
            cols = text.decode("utf8").strip().split("\t")
            if len(cols) != 2:
                continue
            k, v = cols
            word2id[k] = int(v)
        return word2id
 
    def getVocLen(self):
        return len(self.word2id)

    def loadData(self, trainFile):
        data = []
        for text in open(trainFile, "r"):
            cols = text.decode("utf8").strip().split("\t")
            if len(cols) != 3:
                continue
            
            label = int(cols[0])
            query = self.encode(cols[1],self.queryLen)
            doc = self.encode(cols[2],self.docLen)
            data.append([(query, doc), label])
            if len(data) == self.maxSample:
                break
        return data

    def genNegtiveSample(self,negCount):
        newData = []
        for ps in self.data:
            newData.append(ps)
            query = ps[0][0]
            for i in xrange(negCount):
                idx = np.random.randint(len(self.data)-1)
                doc = self.data[idx][0][1]
                ns = [(query,doc),0]
                newData.append(ns)
        self.data = newData

    def encode(self, text,seqLen):
        ids = []
        for w in text.split(" "):
            if w in self.word2id:
                ids.append(self.word2id[w])
            else:
                ids.append(self._UN_)
        
        if len(ids) > seqLen:
            ids = ids[0:seqLen]
        else:
            for i in xrange(seqLen - len(ids)):
                ids.append(self._PAD_)
        
        return np.array(ids)
        
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

def train(model,trainLoader,criterion, optimizer,evalData = None,
            epoch=1,echoStep=100,evalStep=1000,saveStep=5000,savePath="./"):
    
    if evalData != None:
        evalX,evalY = evalData
        if torch.cuda.is_available():
            evalY = evalY.cuda()
            if isinstance (evalX,list):
                for ti,t in enumerate(evalX):
                    evalX[ti] = evalX[ti].cuda()
            else:
                evalX = evalX.cuda()

    for epochIdx in xrange(epoch):
        batchLen = len(trainLoader)
        for i,batch in enumerate(trainLoader,1):
            x, y = batch            
            if torch.cuda.is_available():
                y = y.cuda()
                if isinstance (x,list):
                    for ti,t in enumerate(x):
                        x[ti] = x[ti].cuda()
                else:
                    x = x.cuda()
            out = model(x)
            loss = criterion(out, y)
            
            prob = F.softmax(out, 1) 
            pred = torch.argmax(out, dim=1)
            correct = pred.eq(y).sum()
            acc = float(correct) / len(y)
            
            #print loss
            if i % echoStep == 0:
                print "Step %d/%d/%d : Loss %.4f , Acc %.4f " %(i,batchLen,epochIdx+1,float(loss),acc)
            #evaluate
            if i % evalStep == 0 and evalData != None:
                evalOut = model(evalX)
                evalLoss = criterion(evalOut, evalY)
                correct = torch.argmax(F.softmax(evalOut, 1) , dim=1).eq(evalY).sum()
                evalAcc = float(correct) / len(evalY)
                print "------------------------------------------------"
                print "Evaluate %d Sample : Loss %.4f , Acc %.4f " %(evalY.size(0),float(evalLoss),evalAcc)
                print
            #save model        
            if i % saveStep == 0:
                outFile = "%s/m_%d_%d.pt" %(savePath,i,epochIdx+1)
                torch.save(model.state_dict(),outFile)
                print "Save model : %s" %(outFile)

            #backward
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    outFile = "%s/final.pt" %(savePath)
    torch.save(model.state_dict(),outFile)
    print "Save model : %s" %(outFile)

def main():
    torch.manual_seed(1234)
    np.random.seed(1234)
    queryLen = 10
    docLen = 12
    embDim = 128
    encDim = 256
    print "Load Train Data"
    trainFile = "./data/min_word/train"
    devFile = "./data/min_word/dev"
    vocFile = "./data/min_word/vocab"
    trainData = SimDataset(trainFile,vocFile,queryLen,docLen,2,100000)
    print "Load Dev Data"
    devData = SimDataset(devFile,vocFile,queryLen,docLen,5,10000)

    print "Load Model"
    model = SimLSTMModel(trainData.getVocLen(), embDim, encDim)
    model.load_state_dict(torch.load("./m_5000_10.pt"))
    if torch.cuda.is_available():
        model = model.cuda()
    
    print "Train ... "
    trainLoader = DataLoader(trainData, 100)
    devLoader = DataLoader(devData, 10000)
    devData = None
    for batch in devLoader:
        devData = batch
        break
    #print devData
     
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.9)
    train(model,trainLoader,criterion,optimizer,evalData=devData,epoch=50)

main()
