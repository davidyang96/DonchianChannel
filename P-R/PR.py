# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 10:17:49 2020

@author: yuzhhao
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.preprocessing
from sklearn.metrics import r2_score
from sklearn import linear_model


ho=pd.read_csv('XB-5min.asc',index_col='Date')
ho.index=pd.to_datetime(ho.index)
close=ho['Close'].values.reshape(-1,1)
whole=np.zeros(50)
whole=whole.reshape(-1,1)
b=np.linspace(-0.98,0.98,50)

def pr(t):
    closedifference=np.zeros(len(close)-t)
    for i in range(len(close)-t):
        closedifference[i]=close[i+t]-close[i]

    push=closedifference[0:len(closedifference)-t]
    response=closedifference[t:len(closedifference)]
    pn=sklearn.preprocessing.scale(push)
    rn=sklearn.preprocessing.scale(response)
#x=sorted(pn,reverse=False)
#x=np.array(x)
#y=sorted(push,reverse=False)
#y=np.array(y)
#a=np.arange(-0.20,0.201,0.001)
#b=np.linspace(-0.1995,0.1995,400)
#a=np.arange(-2,2.01,0.01)
#b=np.linspace(-0.1995,0.1995,400)
    a=np.arange(-1,1.02,0.04)
    b=np.linspace(-0.98,0.98,50)
    ra=np.zeros(len(a)-1)
    count=np.zeros(len(a)-1)
    total=np.zeros(len(a)-1)
    for i in range(len(a)-1):
        for j in range(len(push)):
            if a[i]<=pn[j]<a[i+1]:
                total[i]=total[i]+rn[j]
                count[i]=count[i]+1
                if count[i]==0:
                    ra[i]=0
                else:
                    ra[i]=total[i]/count[i]
                        
    for i in range(len(ra)):
        if ra[i]==0:
            ra=np.delete(ra,i,axis=0)
            b=np.delete(b,i,axis=0)

    regr = linear_model.LinearRegression()
    b=b.reshape(-1,1)
    ra=ra.reshape(-1,1)
    regr.fit(b,ra)
    pred=regr.predict(b)
    print('Coefficients: \n', regr.coef_)
    print('Coefficient of determination: %.2f'
      % r2_score(ra,pred))
    c=np.min(b)
    d=np.max(ra)
    e=np.max(count)
    global whole
    whole=np.hstack((whole,ra))
    if t<100:
        t=t/12
    
        plt.figure(figsize=(16,9))
        plt.subplot(211)
        plt.plot(b,ra,color='red',label='real')
        plt.plot(b,pred,color='blue',linewidth=1,label='predict')
        plt.xlabel('Push std')
        plt.ylabel('Response std')
        plt.title('Push-Response')
        plt.legend(loc='lower right')
        plt.text(c,d,r'$alpha=%s$' % regr.coef_ )
        plt.text(c,d-0.01,r'$tau=%s hour(s) $' % t )
        plt.text(c,d-0.02,r'$COD=%s$' % r2_score(ra,pred))
    
        plt.subplot(212)
        plt.scatter(b,count)
        plt.xlabel('Push std')
        plt.ylabel('Frequence for Response')
        plt.text(c,e,r'$mu=|0.02|$')
        plt.show()
    elif t>=100:
        t=t/54
        plt.figure(figsize=(16,9))
        plt.subplot(211)
        plt.plot(b,ra,color='red',label='real')
        plt.plot(b,pred,color='blue',linewidth=1,label='predict')
        plt.xlabel('Push std')
        plt.ylabel('Response std')
        plt.title('Push-Response')
        plt.legend(loc='lower right')
        plt.text(c,d,r'$alpha=%s$' % regr.coef_ )
        plt.text(c,d-0.01,r'$tau=%s days(s) $' % t )
        plt.text(c,d-0.02,r'$COD=%s$' % r2_score(ra,pred))
    
        plt.subplot(212)
        plt.scatter(b,count)
        plt.xlabel('Push std')
        plt.ylabel('Frequence for Response')
        plt.text(c,e,r'$mu=|0.02|$')
        plt.show()

    return
pr(12)
pr(48)
pr(96)
pr(432)
pr(756)
pr(1026)
whole= np.delete(whole,0,axis=1)
plt.figure(figsize=(16,9))
plt.plot(b,whole[:,0],'y',label='1 hour')
plt.plot(b,whole[:,1],'m',label='4 hours')
plt.plot(b,whole[:,2],'c',label='8 hours')
plt.plot(b,whole[:,3],'r',label='8 days')
plt.plot(b,whole[:,4],'darkslateblue',label='14 days')
plt.plot(b,whole[:,5],'b',label='19 days')
plt.legend()
plt.xlabel('Push std')
plt.ylabel('Response std')
plt.title('Push-Response')
ax=plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
#ax.spines['bottom'].set_position(('b', 0))
#ax.spines['left'].set_position(('b',0))
plt.show()

