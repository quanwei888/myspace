#encoding=utf8

import sys
import numpy as np
from keras.preprocessing.sequence import *
from keras.models import *
from keras.layers import *
from keras.layers.embeddings import *
from keras.layers.recurrent import *
from keras.optimizers import *
from sklearn.cross_validation import train_test_split
from optparse import OptionParser 

maxVacabularySize   =   10000
embeddingSize       =   8
chr2idx             =   {}
idx2chr             =   {}
tags                =   ["B","M"]
tag2idx             =   {}
idx2tag             =   {}
NoneChrIdx          =   0
maxSeqLen           =   3
trainFile           =   ""
iterCount			=	1

parser = OptionParser() 
parser.add_option("-t", "--train_file", action="store",dest="train_file",default=False,help=u"数据文件")
parser.add_option("-s", "--seq_size", action="store",dest="seq_size",default=False,help=u"序列长度")
parser.add_option("-i", "--iter_count", action="store",dest="iter_count",default=False,help=u"迭代次数")
(options, args) = parser.parse_args()
if options.train_file == False:
    parser.print_help()
    sys.exit()
if options.seq_size==False:
    parser.print_help()
    sys.exit()
if options.iter_count==False:
    parser.print_help()
    sys.exit()

trainFile = options.train_file
maxSeqLen = int(options.seq_size)
iterCount = int(options.iter_count)

text = open(trainFile).read().decode("utf8")
vacabulary = list(set(w for w in text.replace(" \n","")))
chr2idx = dict((c,i+1) for i,c in enumerate(vacabulary))
chr2idx["NULL"] = 0
idx2chr = dict((v,k) for k,v in chr2idx.items())
idx2chr[0] = "NULL"
tag2idx = dict((t,i) for i,t in enumerate(tags))
idx2tag = dict((v,k) for k,v in tag2idx.items())
maxVacabularySize = len(chr2idx)


def textToSeq(text):
    chrSeq =   []
    tagSeq =   []
    for line in text.split("\n"):
        line = line.strip()
        if line == "":
            continue
        
        chrRow = []
        tagRow = []
        for word in line.split():            
            chrRow.append(word[0:1])
            tagRow.append("B")
            
            for chr in word[1:]:
                chrRow.append(chr)
                tagRow.append("M")
        chrSeq.append(chrRow)
        tagSeq.append(tagRow)
        
    return chrSeq,tagSeq

'''
    charSeq : [["a","b"],["c","d"]]
    tagSeq  : [["b","m"],["b","m"]]
'''
def chrSeqToIntSeq(chrSeq,chr2idx,tagSeq = [],tag2idx = {}):
    chrIntSeq = []
    tagIntSeq = []
    
    for i in range(0,len(chrSeq)):
        chrRow = []
        tagRow = []
        for j in range(0,len(chrSeq[i])):
            chr = chrSeq[i][j]
            if chr2idx.has_key(chr):    
                chrIdx = chr2idx[chr]
            else:
                chrIdx = NoneChrIdx
            chrRow.append(chrIdx)
            
            if len(tagSeq) > 0:
                tag = tagSeq[i][j]
                tagIdx = tag2idx[tag]
                tagRow.append(tagIdx)
        chrIntSeq.append(chrRow)
        tagIntSeq.append(tagRow)
        
    return chrIntSeq,tagIntSeq

def intSeqToTrainData(chrSeq,maxSeqLen = 3,tagSeq = [],tags = []):
    X = []
    Y = []
    
    left = (maxSeqLen-1) / 2
    for i in range(0,len(chrSeq)):
        for j in range(0,len(chrSeq[i])):
            lpos = max(0,j-left)
            rpos = min(len(chrSeq[i]),j-left+maxSeqLen)
            seq = chrSeq[i][lpos:rpos]
            if j-left < 0:
                seq = [0 for k in range(j-left,lpos)] + seq
            if j-left+maxSeqLen >  len(chrSeq[i]):
                seq = seq + [0 for k in range(rpos,j-left+maxSeqLen)]
            X.append(seq)
            
            if len(tagSeq) > 0:
                tag = tagSeq[i][j]
                seq = np.zeros(len(tags))
                seq[tag] = 1.0
                Y.append(seq)
                
    X = pad_sequences(X,padding="post")
    Y = np.asarray(Y)
    
    return X,Y

def pp_intSeqToStr(intSeq):
    for i in range(0,len(intSeq)):
        print "".join([idx2chr[idx] for idx in intSeq[i]])

def pp_result(result):
    for i in range(0,len(result)):
        result[i] = ([1,0] if result[i][0] > result[i][1] else [0,1])
    print result
    
def pp_test(query):
    query = query.replace(" ","")
    X_test,Y_test = textToSeq(query)
    X_test,Y_test = chrSeqToIntSeq(X_test,chr2idx)
    pp_intSeqToStr(X_test)
    X_test,Y_test = intSeqToTrainData(X_test,maxSeqLen)
    result = model.predict(X_test)
    s = ""
    for i in range(0,len(result)):
        s += (" " + query[i] if result[i][0] > result[i][1] else query[i])
    print s

    
X,Y = textToSeq(text)
print "textToSeq"
print X[:3]
print Y[:3]
X,Y = chrSeqToIntSeq(X,chr2idx,Y,tag2idx)
print "chrSeqToIntSeq"
print X[:3]
print Y[:3]
X,Y = intSeqToTrainData(X,maxSeqLen,Y,tags)
print "intSeqToTrainData"
print X[:3]
print Y[:3]

model = Sequential()
model.add(Embedding(input_dim=maxVacabularySize,output_dim=embeddingSize,input_length = maxSeqLen,name="Embedding"))
#model.add(LSTM(100,return_sequences = True,name="LSTM1"))
model.add(LSTM(64,return_sequences = False,name="LSTM2"))
model.add(Dropout(0.5,name="Dropout"))
model.add(Dense(len(tags),name="Dense"))
model.add(Activation('softmax',name="Activation"))

optimizer = Adam(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)


def pp_pinggu():
    train_Y_pred = model.predict(train_X, verbose=0)
    for pred in train_Y_pred:
        if pred[0]>pred[1]:
            pred[0] = 1
            pred[1] = 0
        else:
            pred[0] = 0
            pred[1] = 1
    train_acc = np.sum(train_Y == train_Y_pred, axis=0)[0] / float(train_X.shape[0])
    print('Training accuracy: %.2f%%' % (train_acc * 100))  
    
    test_Y_pred = model.predict(test_X, verbose=0)
    for pred in train_Y_pred:
        if pred[0]>pred[1]:
            pred[0] = 1
            pred[1] = 0
        else:
            pred[0] = 0
            pred[1] = 1
    test_acc = np.sum(test_Y == test_Y_pred, axis=0)[0] / float(test_X.shape[0])
    print('Testing accuracy: %.2f%%' % (test_acc * 100))  
    
    
train_X, test_X, train_Y, test_Y = train_test_split(X, Y , train_size=0.8, random_state=1)
print "Begin Train..."
for i in range(0,iterCount):
    print "-Iteration: " + str(i)
    model.fit(train_X, train_Y, batch_size=128, nb_epoch=1)
    
    train_Y_pred = model.predict(train_X, verbose=0)
    for pred in train_Y_pred:
        if pred[0]>pred[1]:
            pred[0] = 1
            pred[1] = 0
        else:
            pred[0] = 0
            pred[1] = 1    
        
    train_acc = np.sum(train_Y == train_Y_pred, axis=0)[0] / float(train_X.shape[0])
    print('Training accuracy: %.2f%%' % (train_acc * 100))  
    
    test_Y_pred = model.predict(test_X, verbose=0)
    for pred in test_Y_pred:
        if pred[0]>pred[1]:
            pred[0] = 1
            pred[1] = 0
        else:
            pred[0] = 0
            pred[1] = 1
    test_acc = np.sum(test_Y == test_Y_pred, axis=0)[0] / float(test_X.shape[0])
    print('Testing accuracy: %.2f%%' % (test_acc * 100))  
