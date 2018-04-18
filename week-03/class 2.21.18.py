import pandas as pd
import numpy as np
import matplotlib
%matplotlib inline

df=pd.DataFrame()
print(df)

df['name']= ['Bilbo', 'Frodo', 'Samwise']

df
df.assign(height= [0.5, 0.4, 0.6])

df =pd.read_csv('week-03/data/skyhook_2017-07.csv', sep=',')

df.head()
df.shape[1]
df.columns
df['cat_name'].unique()
df['cat_name']
df.cat_name
one_fifty_eight=df[df['hour']==158]
df[(df['hour']==158)& (df['count']>50)].shape
bastille =df[df['date']=='2017-07-14']
bastille.head()
lovers_of_bastille =bastille[bastille['count'] >bastille['count'].mean()]
lovers_of_bastille.describe()
lovers_of_bastille['count'].describe()

df.groupby('date')['count'].sum()
