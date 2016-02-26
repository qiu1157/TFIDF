#!/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 2016年2月23日

@author: qiuxiangu
'''
import math
from operator import itemgetter
from ctypes.test.test_errno import threading
from com.jd.www.v2.myngram import MyNgram
from com.jd.www.v2 import IntegrateTreade
class Worker(object):
    def __init__(self):
        self.input = "e:\\workspace\\SkuClass\\20795.txt"
        self.srcLines = open(self.input,"r" , encoding="utf-8").readlines()
        self.outTfidf = open("bigram.txt", "w+" ,encoding='utf-8')
        self.classOutput="e:\\workspace\\SkuClass\\result\\"
        self.N = 2
        self.myngram = MyNgram(self.N)
        self.flag = False
        
    def CalTF(self):
        #每个类目下每个分词的数量
        self.classRam = {} 
        #每个类目下总分词数
        self.classInfo = {} 
        #每个分词的TF值
        self.classTf = {} 
        #总类目数
        self.alldoc = {} 
        #分词列表
        self.ngram = []
        
    
        for line in self.srcLines:
            columns = line.split("\t")
            #skuId = columns[0]
            skuName = columns[1]
            classId = columns[2]
            #className = columns[3]
            #求有多少类目
            if classId not in self.alldoc:
                self.alldoc[classId] = 1
            
            self.ngram = self.myngram.split(skuName)
            for item in self.ngram:
                ########求类目下词数#########
                if classId not in self.classInfo:
                    self.classInfo[classId] = 1
                    pass
                else:
                    self.classInfo[classId] += 1
                ##########################   
            
               
                if classId not in self.classRam:
                    self.classRam[classId] = {}
                    #####求每个分词的出现次数#####
                    if item not in self.classRam[classId] :
                        self.classRam[classId][item] = 1
                    else:
                        self.classRam[classId][item] += 1
                else:
                    if item not in self.classRam[classId] :
                        self.classRam[classId][item] = 1
                    else:
                        self.classRam[classId][item] += 1
#         print("classInfo---")
#         print(self.classInfo)
#         print("classRam---")
#         print(self.classRam)
        for classId in self.classRam:
            if classId not in self.classTf:
                self.classTf[classId] = {}
                for item in self.classRam[classId]:
                    self.classTf[classId][item] = self.classRam[classId][item] * 1.0 / self.classInfo[classId]
            else:
                for item in self.classRam[classId]:
                    self.classTf[classId][item] = self.classRam[classId][item] * 1.0 / self.classInfo[classId]
        
        if self.flag:
            tffile=open("tffile.txt", "w+" ,encoding='utf-8')
            tffile.write(str(self.classTf))
            tffile.close()

    def CalIDF(self):
        #包含某分词的类目数
        self.keydoc = {}        
        self.classIDF = {}
        for classId in self.alldoc:
            for item in self.classRam[classId]:
                if item not in self.keydoc:
                    self.keydoc[item] = 1
                else:
                    self.keydoc[item] += 1
        
        total = len(self.alldoc)
        for item in self.keydoc:
            self.classIDF[item] = math.log(total / (1+self.keydoc[item]))
            
        if self.flag:
            idffile=open("idffile.txt", "w+" ,encoding='utf-8')
            idffile.write(str(self.classIDF))
            idffile.close()
            
    def CalTFIDF(self):
        self.tfidf = {}
        for classId in self.alldoc:
            self.tfidf[classId] = []
            for item in self.classTf[classId] :
                tf = self.classTf[classId][item]
                idf = self.classIDF[item]
                tfidf = tf * idf
                self.tfidf[classId].append([item, tfidf])
   
            self.tfidf[classId] = sorted(self.tfidf[classId], key = itemgetter(1))
        for classId in self.alldoc:
#             print("classId"==classId)
            for item,tfidf in self.tfidf[classId]:
                line = "%s\t%s\t%s" %(classId,item, str(tfidf))
#                 print("line=="+line)
                self.outTfidf.write(line+"\n")
                 
        self.outTfidf.close()
    
    def merge(self):
        threadingSum = threading.Semaphore(10)
        for classId in self.alldoc:
            t = IntegrateTreade(threadingSum, classId, self.alldoc, self.tfidf, self.srcLines,self.classOutput)
            t.start()
        for t in threading.enumerate():
            if t is threading.currentThread():
                continue
            t.join()
#         self.lineDict = {}
#         for line in self.srcLines:
#             columns = line.split("\t")
#             skuId = columns[0]
#             skuName = columns[1] 
#             classId = columns[2]
#             className = columns[3]
#             self.ngram = self.myngram.split(skuName)
#             score = 0
#             
#             for item in self.ngram:
#                 for rclassId in self.alldoc:
#                     for ram,tfidf in self.tfidf[classId]:
#                         if rclassId == classId and ram == item:
#                             score += tfidf
#             if classId not in self.lineDict:
#                 self.lineDict[classId] = []            
#             self.lineDict[classId].append([className.strip(),skuId,skuName,score]) 
#         
#         for classId in self.alldoc:
#             self.lineDict[classId] = sorted(self.lineDict[classId], key=itemgetter(3), reverse = True)
#             
#         for classId in self.alldoc: 
#             cnt = 0         
#             for className, skuId, skuName, score in self.lineDict[classId]:
#                 cnt += 1
#                 result = "%s\t%s\t%s\t%s\t%s" %(classId, className, skuId, skuName, str(score))
#                 print("result=="+result)
#                 self.outTfidf.write(result+"\n")     
# #                 if cnt > 19 :
# #                     break  
# #             print("result=="+result)
#                     
#         self.outTfidf.close()
        
if __name__ == "__main__":
    w=Worker()
    print("CalTF")
    w.CalTF()
    print("CalIDF")
    w.CalIDF()
    print("CalTFIDF")
    w.CalTFIDF()
    print("merge")
    w.merge()
    print("done!")
            
        
        
                        
                
                    
                 
            