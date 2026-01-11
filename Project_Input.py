#!/usr/bin/env python
# coding: utf-8

# In[1]:


# CAGR of Nifty 50

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


import pandas as pd
import numpy as np
df_Nifty50 = pd.read_csv(os.path.join(DATA_DIR, "Nifty_50.csv"))
df_Nifty50['Date'] = pd.to_datetime(df_Nifty50['Date'])
df_Nifty50 = df_Nifty50.sort_values('Date')

print(df_Nifty50.head())



# In[3]:


initial_value = df_Nifty50['Price'].iloc[0]
final_value = df_Nifty50['Price'].iloc[-1]

n_years = (df_Nifty50['Date'].iloc[-1] - df_Nifty50['Date'].iloc[0]).days / 365.25
cagr_Nifty50 = (final_value / initial_value) ** (1 / n_years) - 1
print("CAGR of Nifty 50 is", cagr_Nifty50*100)


# In[5]:


# CAGR of Nifty Small Cap 50

df_sc50 = pd.read_csv(os.path.join(DATA_DIR, "Smallcap_50.csv"))
df_sc50['Date'] = pd.to_datetime(df_sc50['Date'])
df_sc50 = df_sc50.sort_values('Date')

print(df_sc50.head())



# In[7]:


initial_value_sc50 = df_sc50['Price'].iloc[0]
final_value_sc50 = df_sc50['Price'].iloc[-1]

n_years_sc50 = (df_sc50['Date'].iloc[-1] - df_sc50['Date'].iloc[0]).days / 365.25
cagr_sc50 = (final_value_sc50 / initial_value_sc50) ** (1 / n_years_sc50) - 1
print("CAGR of Nifty Small Cap 50 is", cagr_sc50*100)


# In[9]:


# CAGR of Gold

df_gold = pd.read_csv(os.path.join(DATA_DIR, "Gold.csv"))
df_gold['Year'] = pd.to_datetime(df_gold['Year'], format = '%Y')
df_gold = df_gold.sort_values('Year')

print(df_gold.head())


# In[16]:


initial_value_gold = df_gold['Price'].iloc[0]
final_value_gold = df_gold['Price'].iloc[-1]

n_years_gold = (df_gold['Year'].iloc[-1] - df_gold['Year'].iloc[0]).days / 365.25
cagr_gold = (final_value_gold / initial_value_gold) ** (1 / n_years_gold) - 1
print("CAGR of Gold is", cagr_gold*100)


# In[11]:


# CAGR of Silver

df_silver = pd.read_csv(os.path.join(DATA_DIR, "Silver.csv"))
df_silver['Year'] = pd.to_datetime(df_silver['Year'], format = '%Y')
df_silver = df_silver.sort_values('Year')

print(df_silver.head())


# In[13]:


initial_value_silver = df_silver['Price'].iloc[0]
final_value_silver = df_silver['Price'].iloc[-1]

n_years_silver = (df_silver['Year'].iloc[-1] - df_silver['Year'].iloc[0]).days / 365.25
cagr_silver = (final_value_silver / initial_value_silver) ** (1 / n_years_silver) - 1
print("CAGR of Silver is", cagr_silver*100)


# In[15]:


annuity_rate = 6.0
FD_yield = 7.0



# In[17]:


# CAGR of Midcap 50

import pandas as pd
import numpy as np
df_Midcap_50 = pd.read_csv(os.path.join(DATA_DIR, "Midcap_50.csv"))
df_Midcap_50['Date'] = pd.to_datetime(df_Midcap_50['Date'])
df_Midcap_50 = df_Midcap_50.sort_values('Date')

print(df_Midcap_50.head())

initial_value = df_Midcap_50['Price'].iloc[0]
final_value = df_Midcap_50['Price'].iloc[-1]

n_years = (df_Midcap_50['Date'].iloc[-1] - df_Midcap_50['Date'].iloc[0]).days / 365.25
cagr_Midcap_50= (final_value / initial_value) ** (1 / n_years) - 1
print("CAGR of Midcap 50 is", cagr_Midcap_50*100)

