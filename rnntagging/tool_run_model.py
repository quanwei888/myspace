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
(options, args) = parser.parse_args()
if options.train_file == False:
    parser.print_help()
    sys.exit()
if options.seq_size==False:
    parser.print_help()
    sys.exit()
if options.model_file==False:
    parser.print_help()
    sys.exit()

trainFile = options.train_file
modelFile = options.save_file
maxSeqLen = int(options.seq_size) 

text    =   open(trainFile).read().decode("utf8")
util    =   TaggingUtil()
(X,Y)   =   util.textToTrainData(text,maxSeqLen)

taggingModel   =   TaggingModel()
taggingModel.loadModel(modelFile)

while True:
    query       = sys.stdin.readline().decode("utf8").strip()
    if query == "":
        break
    (qX,qY)     = util.textToTrainData(" ".join([w for w in query]),maxSeqLen)
    qY          = taggingModel.predict(qX)
    result      = util.trainDataToText((qX,qY), maxSeqLen)
    print result