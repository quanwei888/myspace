#encoding=utf8
import sys
sys.path.append("../")

from com.word_helper import WordHelper

query = "南京市长江大桥欢迎你"
query = "乳腺癌早期能活多久"
WordHelper.wordseg(query)
WordHelper.wordrank(query)
WordHelper.wordner(query)
WordHelper.wordpos(query)

query1 = "南京市长江大桥欢迎你"
query2 = "长江大桥在南京"
WordHelper.textsim(query1,query2)