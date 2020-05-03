#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Pipeline for converting raw CICFlowmeter data into model friendly format

import os
import pandas as pd
import numpy as np
from joblib import dump, load
#import requests
from elasticsearch import Elasticsearch

df = pd.read_csv('/home/ubuntu/Malmenator/new_model/packets-record.pcap_Flow.csv')


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


scaler = load('/home/ubuntu/Malmenator/new_model/std_scaler_cicids17.bin')

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


model = load('/home/ubuntu/Malmenator/new_model/rf_cicids2017.joblib') 

y_pred = model.predict(df_out)


# In[5]:


df['predicted'] = y_pred
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format="%d/%m/%Y %I:%M:%S %p")


# In[8]:


es = Elasticsearch("https://search-malmenator-hodt3wt2k7b5x7ph63zibt3eiy.us-east-1.es.amazonaws.com/")


# In[9]:


es


# In[10]:


vals = df.T.to_dict().values()


# In[12]:


for i in vals:
    es.index(index="flows_model", doc_type="_doc", body=i)


# In[ ]:


print("Data sent to ES")

