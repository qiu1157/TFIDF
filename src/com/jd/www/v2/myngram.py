#!/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 2016年2月24日

@author: qiuxiangu
'''
class MyNgram(set):
    def __init__(self, N=0):
        self.N = N
    
    def split(self,string):
        self.str = string
        tmp = ''
        bigram = []
        if self.N == 0 :
            bigram.append(self.str)
        else:
            for item in self.str:
                tmp = tmp+item    
                if(self.N == len(tmp)):
                    bigram.append(tmp)
                    tmp = tmp[1:]
        return bigram
           
        
    
if __name__ =="__main__":
    doc = "东方大幅降低了"
    print(MyNgram(0).split(doc))