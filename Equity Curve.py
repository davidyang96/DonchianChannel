# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 15:56:46 2020

@author: yuzhh
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import random
import sklearn.preprocessing
from pylab import rcParams
import statsmodels.api as sm
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib.dates import DateFormatter, MONDAY, MonthLocator, YearLocator

df=pd.read_csv('XB_8yrs_EC_4Ytrain_4Qtest_EnhanceRS.csv')
df=df.set_index(pd.DatetimeIndex(pd.to_datetime(df['Date']+" "+df['Time'])))
#pd.to_datetime(df.index)
index=df.index.values.reshape(-1,1)
Equity=df['Equity'].values.reshape(-1,1)
fig,ax=plt.subplots(figsize=(16,9))
ax.fmt_xdata=mdates.DateFormatter('%Y-%m-%d')

yearsdays=YearLocator()
mondays=MonthLocator()
#locate=MonthLocator(range(1,2),bymonthday=12,interval=24)
locate=YearLocator(2,month=1,day=3)
ax.xaxis.set_major_locator(locate)
ax.xaxis.set_minor_locator(mondays)
ax.xaxis.set_major_formatter(ax.fmt_xdata)
ax.set_ylabel('Equity')
ax.set_title('Equity Curve for XB with ERS')



a=index[1]
b=np.max(Equity)



ax.plot(index,Equity)
plt.text(a,b,r'$In sample=4 Years$' )
plt.text(a,b-5000,r'$Out sample=4 Quarter(s)$' )
plt.show()
plt.xticks(rotation=45)





