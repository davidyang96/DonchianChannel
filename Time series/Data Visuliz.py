# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 13:50:54 2020

@author: yuzhh
"""

import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams
import statsmodels.api as sm

ho=pd.read_csv('HO-5min.asc',index_col='Date')
ho.index=pd.to_datetime(ho.index)
ho['Heat Oil']=ho['Close']
y=ho['Heat Oil'].resample('W').mean()

rcParams['figure.figsize'] = 16, 9
decomposition = sm.tsa.seasonal_decompose(y, model='additive')
fig = decomposition.plot()
plt.show()
plt.savefig('Heat Oil Visualize')


xb=pd.read_csv('xb-5min.asc',index_col='Date')
xb.index=pd.to_datetime(xb.index)
xb['RBOB']=xb['Close']
y=xb['RBOB'].resample('W').mean()

rcParams['figure.figsize'] = 16, 9
decomposition = sm.tsa.seasonal_decompose(y, model='additive')
fig = decomposition.plot()
plt.show()
plt.savefig('RBOB Visualize')
