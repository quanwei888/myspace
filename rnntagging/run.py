#encoding=utf8

import sys
import numpy as np
from sklearn.cross_validation import train_test_split
from optparse import OptionParser

from tagging_util import TaggingUtil
from tagging_model import TaggingModel

parser = OptionParser()
parser.add_option("-t", "--train_file", action="store",dest="train_file",default=False,help=u"数据文件")
parser.add_option("-m", "--model_file", action="store",dest="model_file",default=False,help=u"模型文件")
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
if options.model_file==False:
    parser.print_help()
    sys.exit()

trainFile = options.train_file
modelFile = options.model_file
maxSeqLen = int(options.seq_size)
iterCount = int(options.iter_count)
    
text    =   open(trainFile).read().decode("utf8")
util    =   TaggingUtil()
(X,Y)   =   util.textToTrainData(text,maxSeqLen)
trainX, testX, trainY, testY = train_test_split(X, Y , train_size=0.8, random_state=1)

taggingModel   =   TaggingModel()
taggingModel.init(len(util.words), len(util.tags), maxSeqLen)

print "----------数据信息---------"
print "    Tag数 ：",len(util.tags)
print "    Word数 ：",len(util.words)
print "    训练样本数 ：",len(X)
print

print "----------数据抽样---------"
print "X ："
print X[:3]
print "Y ："
print Y[:3]
print

print "----------模型结构---------"
for layer in taggingModel.model.layers:
    print "    " + layer.name + "层",":",layer.input_shape,"->",layer.output_shape
print

print "----------训练-------------"
taggingModel.train(trainX,trainY,testX,testY,iterCount) 
print

print "----------保存模型---------"
#taggingModel.saveModel(modelFile)

while True:
    query       = sys.stdin.readline().decode("utf8").strip()
    if query == "":
        break
    (qX,qY)     = util.textToTrainData(" ".join([w for w in query]),maxSeqLen)
    qY          = taggingModel.predict(qX)
    result      = util.trainDataToText((qX,qY), maxSeqLen)
    print result.encode("utf8")