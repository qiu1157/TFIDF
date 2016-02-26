#!/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 2016年2月25日

@author: qiuxiangu
'''
import threading
from operator import itemgetter
from com.jd.www.v2.myngram import MyNgram


class IntegrateTreade(threading.Thread):
    def __init__(self, threadingSum,classId, alldoc, tfidf,srcLines, classOutput):
        threading.Thread.__init__(self)
        #self.input = "e:\\workspace\\SkuClass\\20795.txt"
        #self.srcLines = open(self.input,"r" , encoding="utf-8").readlines()
        self.N = 2
        self.myngram = MyNgram(self.N)
        self.classId = classId
        self.alldoc = alldoc
        self.tfidf = tfidf
        self.outTfidf = None
        self.threadingSum = threadingSum
        self.srcLines = srcLines
        self.classOutput = classOutput
        
    def run(self):
        with self.threadingSum:
            self.lineDict = {}
            print("处理"+self.classId)
            for line in self.srcLines:
                columns = line.split("\t")
                skuId = columns[0]
                skuName = columns[1] 
                classId = columns[2]
                className = columns[3]
                if classId == self.classId:
                    self.ngram = self.myngram.split(skuName)
                    score = 0
                    for item in self.ngram:
                        for ram,tfidf in self.tfidf[self.classId]:
                            if ram == item:
                                score += tfidf
                    if self.classId not in self.lineDict:
                        self.lineDict[self.classId] = []            
                    self.lineDict[self.classId].append([className.strip(),skuId,skuName,score]) 
                
             
                
            self.lineDict[self.classId] = sorted(self.lineDict[self.classId], key=itemgetter(3))  
            cnt = 0     
            for className, skuId, skuName, score in self.lineDict[self.classId]:
                    cnt += 1
                    result = "%s\t%s\t%s\t%s\t%s" %(classId, className, skuId, skuName, str(score))
                    #print("result=="+result)
                    if not self.outTfidf :
                        self.outTfidf = open(self.classOutput+""+className.replace("/","")+"bigram.txt", "w+" ,encoding='utf-8')
                    self.outTfidf.write(result+"\n")
        #                 if cnt > 19 :
        #                     break  
        #             print("result=="+result)
                            
            self.outTfidf.close()
                
            