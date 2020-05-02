# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 16:55:18 2020

@author: yuzhh
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import time
import random
import calendar

HO = pd.read_csv('HO-5min.asc', index_col = 'Date').iloc[:,:5]
HO.index = pd.to_datetime(HO.index)
HO.iloc[:,1:] = HO.iloc[:,1:].multiply(100)
XB = pd.read_csv('XB-5min.asc', index_col = 'Date').iloc[:,:5]
XB.index = pd.to_datetime(XB.index)
XB.iloc[:,1:] = XB.iloc[:,1:].multiply(100)


class DonchianChannel:
    
    def __init__(self,PV,Slpg):
        self.PV = PV
        self.Slpg = Slpg
        self.Transaction = []
    
    def buy(self):
        self.market_position += 1
        
    def sell(self):
        self.market_position -= 1
            
    def EquityCurve(self,data,ChnLen,StpPct, maxbar = 0): 
        
        ##Equity curve of data start at ChnLen-th point with StopLoss of StpPct
        ##Output: A series of portfolio value
        
        portfolio_value = 100000
        
        HighestHigh = np.array(data.High.rolling(ChnLen).max())
        LowestLow = np.array(data.Low.rolling(ChnLen).min())
        n = len(data)
        val = np.zeros(n)+100000
        
        market_position = 0
        PrevPeak = 0
        PrevTrough = 0
        
        Date = np.array(data.index)
        Time = np.array(data.Time)
        Open = np.array(data.Open)
        High = np.array(data.High)
        Close = np.array(data.Close)
        Low = np.array(data.Low)
        
        if maxbar == 0:
            maxbar = ChnLen
        
        for i in range(maxbar,n):
            
            if market_position == 0:

                if High[i] >= HighestHigh[i]:
                    market_position += 1
                    EntryPrice = HighestHigh[i]
                    PrevPeak = HighestHigh[i]
                    self.Transaction.append(['long',Date[i],Time[i],EntryPrice])
                    val[i:] -= self.Slpg/2  
                    
                elif Low[i] <= LowestLow[i]:
                    market_position -= 1
                    EntryPrice = LowestLow[i]
                    PrevTrough = LowestLow[i]
                    self.Transaction.append(['short',Date[i],Time[i],EntryPrice])
                    val[i:] -= self.Slpg/2
                    
            if market_position > 0:
                if Close[i] >= PrevPeak:
                    PrevPeak = Close[i]
                    val[i] += (Close[i] - EntryPrice)*self.PV
                elif Low[i] <= PrevPeak*(1-StpPct):
                    market_position -= 1
                    self.Transaction.append(['end long',Date[i],Time[i],PrevPeak*(1-StpPct)])
                    val[i] += (PrevPeak*(1-StpPct) - EntryPrice)*self.PV - self.Slpg/2
                    val[i+1:] = val[i]
                else:
                    val[i] += (Close[i] - EntryPrice)*self.PV
                
            elif market_position < 0:
                if Close[i] <= PrevTrough:
                    PrevTrough = Close[i]
                    val[i] += -(Close[i] - EntryPrice)*self.PV
                elif High[i] >= PrevTrough*(1+StpPct):
                    market_position += 1
                    self.Transaction.append(['end short',Date[i],Time[i],PrevTrough*(1+StpPct)])
                    val[i] += -(PrevTrough*(1+StpPct) - EntryPrice)*self.PV - self.Slpg/2
                    val[i+1:] = val[i]
                else:
                    val[i] += -(Close[i] - EntryPrice)*self.PV
        
        if market_position > 0:
            self.Transaction.append(['end long',Date[i],Time[i],Close[i]])
            val[-1] += -self.Slpg/2
        elif market_position < 0:
            self.Transaction.append(['end short',Date[i],Time[i],Close[i]])
            val[-1] += -self.Slpg/2
            
        return val
       
    def performance(self,Open,High,Close,Low,HighestHigh,LowestLow,ChnLen,StpPct,method ='roa'):
        
        ##Input: np.array - Open,High,Close,Low,HighestHigh,LowestLow
        ##            int - ChnLen
        ##          float - StpPct
        ##         method - 'roa' or 'RoMaD'
        ##Output:   score of our strategy
        
        n = len(Open)
        market_position = 0
        EntryPrice = 0
        PrevPeak = 0
        PrevTrough = 0
        val = np.zeros(n)+100000
        
        n = len(Open)
        prev_max = 0
        maximum_drawdown = 0
        
        for i in range(ChnLen,n):
            
            if market_position == 0:

                if High[i] >= HighestHigh[i]:
                    market_position += 1
                    EntryPrice = HighestHigh[i]
                    PrevPeak = HighestHigh[i]
                    val[i:] -= self.Slpg/2  
                    
                elif Low[i] <= LowestLow[i]:
                    market_position -= 1
                    EntryPrice = LowestLow[i]
                    PrevTrough = LowestLow[i]
                    val[i:] -= self.Slpg/2
                    
            if market_position > 0:
                if Close[i] >= PrevPeak:
                    PrevPeak = Close[i]
                    val[i] += (Close[i] - EntryPrice)*self.PV
                elif Low[i] <= PrevPeak*(1-StpPct):
                    market_position -= 1
                    val[i] += (PrevPeak*(1-StpPct) - EntryPrice)*self.PV - self.Slpg/2
                    val[i+1:] = val[i]
                else:
                    val[i] += (Close[i] - EntryPrice)*self.PV
                
            elif market_position < 0:
                if Close[i] <= PrevTrough:
                    PrevTrough = Close[i]
                    val[i] += -(Close[i] - EntryPrice)*self.PV
                elif High[i] >= PrevTrough*(1+StpPct):
                    market_position += 1
                    val[i] += -(PrevTrough*(1+StpPct) - EntryPrice)*self.PV - self.Slpg/2
                    val[i+1:] = val[i]
                else:
                    val[i] += -(Close[i] - EntryPrice)*self.PV
            
            if val[i] > prev_max:
                prev_max = val[i]
            drawdown = max(0,prev_max-val[i])
            if drawdown > maximum_drawdown:
                maximum_drawdown = drawdown
                
        profit = val[-1]-100000
        
        if maximum_drawdown == 0:
            print(val)
        if method == 'roa':
            return profit
        elif method == 'RoMaD':
            return profit/maximum_drawdown
               
    def fit_random_search(self,data,max_iteration,method='roa'):
        
        ## Intput: pd.DataFrame - data
        ##                  int - max_iteration
        ##               string - method
        ## Output: tuple of parameters of Chn and StpPct
        
        Open = np.array(data.Open)
        High = np.array(data.High)
        Close = np.array(data.Close)
        Low = np.array(data.Low)
               
        Best_Chn = 0
        Best_StpPct = 0
        b_score = 0
        
        for i in range(max_iteration):
            Chn = np.random.randint(5,101)*100
            StpPct = np.random.randint(5,101)/1000
            HighestHigh = np.array(data.High.rolling(Chn).max())
            LowestLow = np.array(data.Low.rolling(Chn).min())
            score = self.performance(Open,High,Close,Low,HighestHigh,LowestLow,Chn,StpPct,method)
        
            if score > b_score:
                Best_Chn = Chn
                Best_StpPct = StpPct
                b_score = score
            
        return (Best_Chn,Best_StpPct)    

data = HO[(HO.index > datetime(2009,1,1)) & (HO.index < datetime(2020,1,1))]

np.random.randint(5,101,100)
    
def maxDD(array):
    prevmax = 0
    MDD = 0
    n = len(array)
    for i in range(n):
        if array[i] > prevmax:
            prevmax = array[i]
        DD = max(0,prevmax - array[i])
        if DD > MDD:
            MDD = DD
    return MDD


StpPct = np.random.randint(5,101,100)/1000   
max_bar = 16953





a = DonchianChannel(420,70)
ChnLen = 5020

Perfor = []
for i in range(100):
    ec = a.EquityCurve(data,ChnLen,StpPct[i],maxbar=max_bar)
    Perfor.append(ec[-1]/maxDD(ec))

plt.scatter(StpPct,Perfor)    


c=np.zeros(100)
c[:]=ChnLen

   
d=np.column_stack((c,Perfor))   
    
e=np.column_stack((e,d))
    
    
   
    
    
    
    
    
    
    
    
    
    
    
    
    


    
    
    
    
    
    
    

