# encoding=utf8

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

class TaggingModel:
    model = None
    
    embSize = 8
    lstmOutDim = 32
    dropOut = 0.5
    optimizerLr = 0.01
    
    def __init__(self):
        pass
    
    def init(self, wordsCount, tagsCount, maxSeqLen):
        model = Sequential()
        model.add(Embedding(input_dim=wordsCount+1, output_dim=self.embSize, input_length=maxSeqLen, name="Embedding"))
        model.add(LSTM(self.lstmOutDim, return_sequences=False, name="LSTM"))
        model.add(Dropout(self.dropOut, name="Dropout"))
        model.add(Dense(tagsCount, name="Dense"))
        model.add(Activation('softmax', name="Activation"))
        optimizer = Adam(lr=self.optimizerLr)
        model.compile(loss='categorical_crossentropy', optimizer=optimizer)
        
        self.model = model
    
    def loadModel(self,path):
        self.model = load_model(path)
        
    def saveModel(self,path):
        self.model.save(path)
    
    def train(self,X,Y,testX,testY,iterCount = 5,batchSize = 128):
        for i in range(0,iterCount):
            self.model.fit(X, Y, batch_size=batchSize, nb_epoch=1)
            Y1 = self.model.predict(X, verbose=0)
            print('训练集-准确率: %.2f%%' % (self.getAccuracy(Y,Y1) * 100))
            Y1 = self.model.predict(testX, verbose=0)
            print('测试集-准确率: %.2f%%' % (self.getAccuracy(testY,Y1) * 100))
    def getAccuracy(self,Y,Y1):
        Y   = np.asarray([np.argmax(y) for y in Y])
        Y1  = np.asarray([np.argmax(y) for y in Y1])
        accuracy = np.sum(Y1 == Y) / float(len(Y))
        return accuracy
    
    def predict(self,X):
        Y = self.model.predict(X, verbose=0)
        Y   = np.asarray([np.where(y>=np.max(y),1,0) for y in Y])
        return Y