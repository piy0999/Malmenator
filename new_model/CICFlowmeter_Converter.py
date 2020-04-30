#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Pipeline for converting raw CICFlowmeter data into model friendly format

import os
import pandas as pd
import numpy as np
from joblib import dump, load

df = pd.read_csv('packets-record.pcap_Flow.csv')


# In[2]:


# Reengineer ports
df['is_well_known_port'] = df.apply(lambda row: 1 if row['Dst Port'] < 1024 else 0, axis=1)
df['is_registered_port'] = df.apply(lambda row: 1 if row['Dst Port'] >= 1024 and row['Dst Port'] < 49152 else 0, axis=1)

# Drop certain columns

cols_to_drop = ['Flow ID', 'Src IP', 'Src Port', 'Dst IP', 'Dst Port', 'Protocol',
                'Timestamp', 'Bwd PSH Flags', 'Bwd URG Flags', 'Fwd Byts/b Avg', 'Fwd Pkts/b Avg',
                'Fwd Blk Rate Avg', 'Bwd Byts/b Avg', 'Bwd Pkts/b Avg', 'Bwd Blk Rate Avg', 'Label']

df_out = df.drop(columns=cols_to_drop, axis=1)

# Reorganize column order


# Scale columns


# In[3]:


scaler = load('std_scaler_cicids17.bin')

cols = list(df_out.columns.values)
cols.remove('Fwd PSH Flags')
cols.remove('Fwd URG Flags')
cols.remove('FIN Flag Cnt')
cols.remove('SYN Flag Cnt')
cols.remove('RST Flag Cnt')
cols.remove('PSH Flag Cnt')
cols.remove('ACK Flag Cnt')
cols.remove('URG Flag Cnt')
cols.remove('CWE Flag Count')
cols.remove('ECE Flag Cnt')
cols.remove('is_well_known_port')
cols.remove('is_registered_port')

df_out[cols] = scaler.transform(df_out[cols])


# In[4]:


model = load('rf_cicids2017.joblib') 

y_pred = model.predict(df_out)


# In[5]:


df['predicted'] = y_pred
df['Timestamp'] = pd.to_datetime(df['Timestamp'])


# In[7]:


df.to_csv('model_output.csv', header=False, index=False)


# In[ ]:




