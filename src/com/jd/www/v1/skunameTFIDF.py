#!/bin/python3
# -*- coding: utf-8 -*-

import math
from idlelib.IOBinding import encoding


class SkuNameTFIDF(object):
    def __init__(self):
        self.input = "e:\\workspace\\SkuClass\\sku20160221.csv"
        self.out_tfidf = open("out_tfidf.txt", "w+")
        self.lines = open(self.input,"r", encoding="utf-8").readlines()
        #self.association_out = open("tfidf_out_"+self.input, "w+")
        self.total_cnt = len(self.lines)
        self.doc_index = 2
        self.word_index = 1
        self.err_cnt = 0
        
    def CalTF(self):
        self.tf = {}
        self.wd_fre = {}
        self.wd_tf = {}
        self.classInfo = {}
        for line in self.lines:
            #line = line.decode("gbk").encode("utf8")
            splits = line.strip('\n').split(",")
            group_field = splits[self.doc_index]+"\t"+splits[3]
            item_fileld = splits[self.word_index]
            
            #每个类目下商品数
            if group_field not in self.classInfo:
                self.classInfo[group_field] = 1
            else:
                self.classInfo[group_field] += 1
                
#             if item_fileld not in self.wd_fre :
#                 self.wd_fre[item_fileld] = 1
#             else :
#                 self.wd_fre[item_fileld] += 1
            #每个类目下每个商品数
            if group_field not in self.tf :
                self.tf[group_field] = {}
            if item_fileld not in self.tf[group_field] :
                self.tf[group_field][item_fileld] = 1
            else :
                self.tf[group_field][item_fileld] +=1
                   
        for gp in self.tf :
            if gp not in self.wd_tf :
                self.wd_tf[gp] = {}
                for item in self.tf[gp] :
                    self.wd_tf[gp][item] = self.tf[gp][item] * 1.0 / self.classInfo[gp]
            else:
                for item in self.tf[gp]:
                    self.wd_tf[gp][item] = self.tf[gp][item] * 1.0 / self.classInfo[gp]
#         print(self.wd_tf)          
#         for gp in self.wd_tf :
#             for item in self.wd_tf[gp] :
#                 pass
#         pass
    
    def CalIDF(self):
        self.wd_docs = {}
        self.all_docs = {}
        self.wd_idf = {}
        for line in self.lines :
            #line = line.decode("gbk").encode("utf8")
            splits = line.strip('\n').split(",")
            
            group_field = splits[self.doc_index]+"\t"+splits[3]
            item_field = splits[self.word_index]
            
            if group_field not in self.wd_docs :
                self.all_docs[group_field] = 1
            if item_field not in self.wd_docs :
                self.wd_docs[item_field] = {}
                if group_field not in self.wd_docs[item_field] :
                    self.wd_docs[item_field][group_field] = 1
            else :
                if group_field not in self.wd_docs[item_field] :
                    self.wd_docs[item_field][group_field] = 1
     
        for wd in self.wd_docs :
            idfval = math.log(len(self.all_docs) / (1+len(self.wd_docs[wd])))
            self.wd_idf[wd] = idfval

            
    def CalTFIDF(self):
        self.tfidf = {}
        for gp in self.wd_tf :
            if gp not in self.tfidf :
                self.tfidf[gp] = []
            for item in self.wd_tf[gp] :
                tf = self.wd_tf[gp][item]
                idf = self.wd_idf[item]
                tfidf = tf*idf
                self.tfidf[gp].append([item, tfidf])
            
            special_sort = lambda x :x[1]
            
            self.tfidf[gp] = sorted(self.tfidf[gp] , key = special_sort)
            
        for gp in self.tfidf :
            cnt = 0
            max_out = 10
            for item, score in self.tfidf[gp] :
                line = "%s\t%s\t%s" %(gp,item,str(score))
                self.out_tfidf.write(line+"\n")
                cnt += 1
                if cnt>max_out:
                    break
        self.out_tfidf.close()
    def Run(self):
        self.CalTF()
        self.CalIDF()
        self.CalTFIDF()
        print ("process done!")
        pass       
        
            
            
if __name__ == '__main__':
    SkuNameTFIDF().Run()            