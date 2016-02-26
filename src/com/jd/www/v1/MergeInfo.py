#!/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 2016年2月22日

@author: qiuxiangu
'''
class MergeInfo(object):
    def __init__(self):
        self.srcFile = "e:\\workspace\\SkuClass\\sku20160222"
        self.resultFile = "e:\\workspace\\SkuClass\\src\\算法1_skuname计算_优化.txt"
        self.srcHandle = open(self.srcFile,"r", encoding="utf-8").readlines()
        self.resultHandle = open(self.resultFile,"r", encoding="utf-8").readlines()
        self.outHandle = open("out_1.txt", "w+")
    
    def srcDict(self):
        self.srcdict = {}
        for srcLine in self.srcHandle :   
            srcClassId = srcLine.split("\t")[2]
            srcSkuName = srcLine.split("\t")[1]
            if srcClassId not in self.srcdict:
                self.srcdict[srcClassId] = {}
                if srcSkuName not in self.srcdict[srcClassId]:
                    self.srcdict[srcClassId][srcSkuName] =  srcLine
                else:
                    self.srcdict[srcClassId][srcSkuName] =  srcLine
            else:
                if srcSkuName not in self.srcdict[srcClassId]:
                    self.srcdict[srcClassId][srcSkuName] =  srcLine
                else:
                    self.srcdict[srcClassId][srcSkuName] =  srcLine
        print("源数据装载完毕")
    def merge(self):
        for resultLine in self.resultHandle :
            classid = resultLine.split("\t")[0]
            skuname = resultLine.split("\t")[2]
            #print(classid +"\t"+skuname)
            if classid in self.srcdict:
                for item in self.srcdict[classid] :
                    #print(item)
                    srcSkuName = item
                    if  skuname == srcSkuName : 
                        self.outHandle.write(self.srcdict[classid][item])
                    
        self.outHandle.close()
        print("process done!")            
if __name__ == '__main__' :
    m=MergeInfo()
    m.srcDict()
    m.merge()     
                