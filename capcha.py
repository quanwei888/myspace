# -*- coding: utf-8 -*-

from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random
import math

#背景色
BACKGROUND_COLOR=0
#前景色
COLOR = 200

#裁剪图片，保留前景色所需的最小尺寸
def resize(img):
    data = getPoint(img)

    #获取4个方向的最边缘的坐标
    leftX = min(data,key=lambda p:p[0])[0]
    rightX = max(data,key=lambda p:p[0])[0]
    topY = min(data,key=lambda p:p[1])[1]
    bottomY = max(data,key=lambda p:p[1])[1]

    #裁剪
    chrImg = img.crop((leftX,topY,rightX,bottomY))
    return chrImg

#获取所有前景色像素点
def getPoint(img):
    data = []
    for i in xrange(img.width):
        for j in xrange(img.height):
            if img.getpixel((i,j)) == COLOR:
                data.append((i,j))
    return data

#得到图像的边界像素点
def getEdgePoint(img):
    edgeImg = img.filter(ImageFilter.FIND_EDGES)
    edgeImg.save("e.png")
    #edgeImg.show()
    leftData = []
    topData = []
    rightData = []
    bottomData = []

    #左边界
    for i in xrange(edgeImg.height):
        for j in xrange(edgeImg.width):
            color = edgeImg.getpixel((j,i))
            if color != BACKGROUND_COLOR:
                leftData.append((j,i))
                break
    #右边界
    for i in xrange(edgeImg.height):
        for j in range(edgeImg.width-1,0,-1):
            color = edgeImg.getpixel((j,i))
            if color != BACKGROUND_COLOR:
                rightData.append((j,i))
                break
    
    #上边界
    for i in xrange(edgeImg.width):
        for j in xrange(edgeImg.height):
            color = edgeImg.getpixel((i,j))
            if color != BACKGROUND_COLOR:
                topData.append((i,j))
                break
    
    #下边界
    for i in xrange(edgeImg.width):
        for j in range(edgeImg.height-1,0,-1):
            color = edgeImg.getpixel((i,j))
            if color != BACKGROUND_COLOR:
                bottomData.append((i,j))
                break

    return (leftData,topData,rightData,bottomData)

#給定點集,求所有合法斜率,mask設定方向,1爲右,-1爲左
def getSlope(data,mask):
    result = []
    for i in xrange(len(data)):
        for j in range(i+1,len(data)):
            p1 = data[i]
            p2 = data[j]
            if p1[0] == p2[0]:
                continue
            
            #计算slope,y=k(x-x1)+y1
            k = float((p1[1]-p2[1]))/(p1[0]-p2[0])
            #print k
            #判断有没有点在直线右边/右边
            valid = True
            for p in data:
                v = (k * (p[0]-p1[0])+p1[1] - p[1]) * mask
                #print p1,p,v,k
                if (v > 0):
                    valid = False
                    break

            if valid:
                if abs(p1[1]-p2[1]) < 10:
                    continue
                normDegree = int(math.atan(k)/math.pi*180)
                if normDegree < 0:
                    normDegree = 180+normDegree
                if normDegree > 90:
                    leftDegree = 0
                    rightDegree = 180- normDegree 
                else:
                    leftDegree = 90-normDegree
                    rightDegree = 0
                result.append((p1,p2,leftDegree,rightDegree))
    return result

#左邊界構成合法斜率的點集
def getLeftSlope(data):
    return getSlope(data,1)

#左邊界構成合法斜率的點集
def getRightSlope(data):
    return getSlope(data,-1)

#生成文本圖片
def getTextImage(text,size = 100):
    img = Image.new('L',(size * len(text),size*2),BACKGROUND_COLOR)
    drawImg = ImageDraw.Draw(img)
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansOblique.ttf", size)
    drawImg.text((0,0), text, font=fnt, fill=COLOR)
    return img

#旋转并缩放
def rotateAndResize(img,deegre):
    return resize(img.rotate(deegre,expand=1))

#复制图片
def copy(dest,src,pos):
    for i in xrange(src.width):
        for j in xrange(src.height):
            color = src.getpixel((i,j))
            if color == BACKGROUND_COLOR:
                continue
            dest.putpixel((pos[0] + i,pos[1]+j),color)

#IMG2相對IMG1垂直方向移動
def verticalMove(img1,img2,size):
    if size > 0:
        #向下移動
        newHeight = size+img2.height
        newImg = Image.new('L',(img2.width,newHeight),BACKGROUND_COLOR)
        copy(newImg,img2,(0,abs(size)))
        return img1,newImg
    else:
        #向上移動
        newHeight = abs(size)+img1.height
        newImg = Image.new('L',(img1.width,newHeight),BACKGROUND_COLOR)
        copy(newImg,img1,(0,abs(size)))
        return newImg,img2

#粘接2个图片
def concatImages(img1,img2,deep=2):

    #img2随机上下移动
    img1,img2 = verticalMove(img1,img2,random.randint(-20,20))

    left,top,right,bottom =  getEdgePoint(img1)
    data1 =  left+top+right+bottom 
    left,top,right,bottom =  getEdgePoint(img2)
    data2 =  left+top+right+bottom

    data2 = [(pos[0]+img1.width,pos[1]) for pos in data2]

    #试图左移动,直到交集
    step = 1
    for i in range(0,img1.width,step):
        tmpDataSet2 = set([(pos[0]-i,pos[1]) for pos in data2])
        interSet = set(data1).intersection(tmpDataSet2)
        #print interSet,i
        if len(interSet)>0:
            break
    xdelta = deep + i
    newImg = Image.new('L',(img2.width+img1.width-xdelta,max(img1.height,img2.height)),BACKGROUND_COLOR)
    copy(newImg,img1,(0,0))
    copy(newImg,img2,(img1.width-xdelta,0))
    return newImg

#扭曲图片
def tortuousAndResize(img):
    w,h = img.size
    f = 6.28 / h *0.5
    newImg = Image.new('L',(img.width+20,img.height),0)
    #print img.size,newImg.size
    for i in range(1,h):
        detaX = int(10 * (0 + math.cos(i*f)))
        for j in range(10,w):
            color = img.getpixel((j,i))
            newImg.putpixel((j+detaX+10,i),color)
    newImg.show()
    return resize(newImg)

def canRotateDegree(img,type="LEFT"):
    data = getEdgePoint(img)
    if type=="LEFT":
        slopes = getLeftSlope(data[0])
        #D
    else:
        slopes = getRightSlope(data[2])
    print slopes
    if slopes == []:
        left = 0
    else:
        leftPoint = max(slopes,key=lambda p:p[2])
        left = leftPoint[2]
    
    #print slopes,degreePoint
    if slopes == []:
        right = 0
    else:
        rightPoint = max(slopes,key=lambda p:p[3])
        right = rightPoint[3]
    
    return left,right
def leftCanRotateDegree(img):
    return canRotateDegree(img,"LEFT")
def rightCanRotateDegree(img):
    return canRotateDegree(img,"RIGHT")

'''
img = resize(getTextImage("A",100))
img.show()
leftDegree,rightDegree = leftCanRotateDegree(img) 
print leftDegree,rightDegree
#print rightCanRotateDegree(img) 
'''

category = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM123456789"
text = ""
for i in xrange(4):
    text += category[random.randint(0,len(category)-1)]

#text="AB"
imgs = [resize(getTextImage(chr,random.randint(80,100))) for chr in text]
img = imgs[0]
degree = random.randint(-30,30)
img = rotateAndResize(img,degree)
for i in range(1,len(imgs)):
    #data = getEdgePoint(img)
    #slopes = getRightSlope(data[2])
    left1,right1 = rightCanRotateDegree(img)
    left2,right2 = leftCanRotateDegree(imgs[i])
    print 11111,left1,right1
    print 11111,left2,right2
    #imgs[i].show()
    
    left = left1 + left2
    right = right1 + right2
        

    if left > right:
        imgs[i] = rotateAndResize(imgs[i],min(30,left))
        print left
    else:
        imgs[i] = rotateAndResize(imgs[i],-min(30,right))
        print -right

    #imgs[i].show()
    img = concatImages(img,imgs[i])
    

img = tortuousAndResize(img)
img.save("4.png")
print text
#img.show() 
