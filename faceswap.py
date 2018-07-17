#coding=utf-8

import pdb
import cv2
import dlib
import sys
import numpy as np 
 
#初始化
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")

#获取人脸的68个关键特征点
def getLandmarkPoints(img):
    results = detector(img, 1)
    if len(results) == 0:
        raise Exception("Did not found the face in image")
    if len(results) > 1:
        raise Exception("found more than 1 faces in image")
    
    shape = predictor(img, results[0])
    points = []
    for part in shape.parts():
        points.append((int(part.x),int(part.y)))
    if len(points) != 68:
        raise Exception("found less than 68 landmark in face")

    return np.int32(points)

#获取凸包
def getConvexHullPoints(points):
    ids = cv2.convexHull(np.array(points), returnPoints = False)
    convexHullPoints = []
    for i in ids:
        convexHullPoints.append(points[i[0]])
    return np.int32(convexHullPoints)

#点是否在矩形框里
def rectContains(rect, point) :
    if point[0] < rect[0] :
        return False
    elif point[1] < rect[1] :
        return False
    elif point[0] > rect[2] :
        return False
    elif point[1] > rect[3] :
        return False
    return True

#获取三角剖分后的三角块
def getDelaunayTriangles(points) :
    #获取点的边界
    convexHullPoints = getConvexHullPoints(points)
    #print convexHullPoints
    rec = cv2.boundingRect(np.int32([convexHullPoints]))
    #print rec
    subdiv = cv2.Subdiv2D((0, 0, rec[0]+rec[2],rec[1]+rec[3]))
    for point in points:
        #print point,rec,(0, 0, rec[0]+rec[2],rec[1]+rec[3])
        subdiv.insert((point[0],point[1]))

    triangles = subdiv.getTriangleList()
    validTriangles = []
    for triangle in triangles :
        pt1 = (triangle[0], triangle[1])
        pt2 = (triangle[2], triangle[3])
        pt3 = (triangle[4], triangle[5])
        if  pt1 not in points or pt2 not in points or pt3 not in points:
            continue
        validTriangles.append(np.int32([pt1,pt2,pt3]))
        #print np.int32([pt1,pt2,pt3])
    return np.int32(validTriangles)

#获取帶索引的三角块，索引：Point1ID_Point2ID_Point3ID
def getIndexTriangles(points,triangles):
    point2id = {}
    for i,point in enumerate(points):
        key = "_".join([str(x) for x in point])
        point2id[key] = i

    triangleDict = {}
    for i,triangle in enumerate(triangles):
        triangleKey = []
        for j in xrange(3):
            pointKey = "_".join([str(x) for x in triangle[j]])
            if pointKey not in point2id:
                print triangle[j]
                raise Exception(pointKey + " key not found" )
            triangleKey.append(point2id[pointKey])
        triangleKey = "_".join([str(x) for x in triangleKey])
        triangleDict[triangleKey] = triangle

    return triangleDict

#融合
def morph(srcImg,dstImg,srcTriangle,dstTriangle,alpha=0):
    #计算变形矩形区域
    srcRec = cv2.boundingRect(np.int32([srcTriangle]))
    dstRec = cv2.boundingRect(np.int32([dstTriangle]))
    
    #保存待变形区域的三角块，从(0,0)开始，用于计算仿射矩阵
    srcNewTraingle = []
    dstNewTraingle = []
    for i in xrange(0, 3):
        srcNewTraingle.append(((srcTriangle[i][0] - srcRec[0]),(srcTriangle[i][1] - srcRec[1])))
        dstNewTraingle.append(((dstTriangle[i][0] - dstRec[0]),(dstTriangle[i][1] - dstRec[1])))
    #计算仿射矩阵
    warpMat = cv2.getAffineTransform( np.float32(srcNewTraingle), np.float32(dstNewTraingle) )

    #保存待变形区域的图像
    srcCroppedImg = srcImg[srcRec[1]:srcRec[1] + srcRec[3], srcRec[0]:srcRec[0] + srcRec[2]]
    dstCroppedImg = dstImg[dstRec[1]:dstRec[1] + dstRec[3], dstRec[0]:dstRec[0] + dstRec[2]]
    
    #cv2.imwrite("1.png",srcCroppedImg)
    #cv2.imwrite("2.png",dstCroppedImg)

    #仿射变换，这里整个srcRec区域的变换
    outputTraingleImg = cv2.warpAffine( srcCroppedImg, warpMat, (dstRec[2], dstRec[3]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )
    #print (srcRec, dstRec)
    #print (srcTriangle, dstTriangle)
    #通过Mask来完成仅三角区域变换
    dstMask = np.zeros((dstRec[3], dstRec[2], 3), dtype = np.float32)
    #将目标图像的三角区域填充为1,其余为0，并完成Mask制作
    cv2.fillConvexPoly(dstMask, np.int32([dstNewTraingle]), (1, 1, 1), 16, 0);
    #将三角区块外置为0，同时三角区域内融合双方颜色，由alpha控制权重
    outputTraingleImg = outputTraingleImg * dstMask * (1-alpha) + dstCroppedImg * dstMask *alpha
    #cv2.imwrite("5.png",outputTraingleImg)
    #在dstImg中将矩形块的颜色应用mask，将三角区域内置为0
    dstImg[dstRec[1]:dstRec[1]+dstRec[3], dstRec[0]:dstRec[0]+dstRec[2]] = dstImg[dstRec[1]:dstRec[1]+dstRec[3], dstRec[0]:dstRec[0]+dstRec[2]] * ( (1.0, 1.0, 1.0) - dstMask )
    #cv2.imwrite("1.png",dstImg)
    #合并，完成整体融合
    dstImg[dstRec[1]:dstRec[1]+dstRec[3], dstRec[0]:dstRec[0]+dstRec[2]] = dstImg[dstRec[1]:dstRec[1]+dstRec[3], dstRec[0]:dstRec[0]+dstRec[2]] + outputTraingleImg
    #cv2.imwrite("2.png",dstImg)

#seamlessClone
def seamlessClone(srcImg,dstImg,dstPoints):
    polyPoints = getConvexHullPoints(dstPoints)
    srcMask = np.zeros(srcImg.shape, srcImg.dtype)
    cv2.fillPoly(srcMask, np.array([polyPoints]), (255, 255, 255))
    rec = cv2.boundingRect(np.array([polyPoints]))
    center = ((rec[0] + rec[2]/2),(rec[1] + rec[3]/2))
    output = cv2.seamlessClone(srcImg, dstImg, srcMask, center, cv2.NORMAL_CLONE)
    return output


print "CMD USAGE:   faceswap img1 img2 "
srcImg = cv2.imread(sys.argv[1])
dstImg = cv2.imread(sys.argv[2])

srcPoints = getLandmarkPoints(srcImg)
dstPoints = getLandmarkPoints(dstImg)

srcTriangles = getDelaunayTriangles(srcPoints)
dstTriangles = getDelaunayTriangles(dstPoints)
#print "Triangles Length",len(srcTriangles),len(dstTriangles)
dstIndexTriangle = getIndexTriangles(dstPoints,dstTriangles)

for key,dstTriangle in dstIndexTriangle.items():
    ids = [int(x) for x in key.split("_")]
    srcTriangle = [srcPoints[ids[0]],srcPoints[ids[1]],srcPoints[ids[2]]]
    morph(srcImg,dstImg,srcTriangle,dstTriangle,0.2)
    #break
cv2.imwrite("out_swap.png",dstImg)

#seamless clone
rawDstImg = cv2.imread(sys.argv[2])
seamlessImg = seamlessClone(dstImg,rawDstImg,dstPoints)
cv2.imwrite("out_seamless.png",seamlessImg)
