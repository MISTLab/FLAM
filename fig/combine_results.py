#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df_crm = pd.read_csv('crm.csv')
t = df_crm['t']

df_knn = pd.read_csv('knn.csv')
t2 = df_knn['t']

avg = np.interp(t, t2, df_knn['avg'])

dmin = np.interp(t, t2, df_knn['dmin'])
davg = np.interp(t, t2, df_knn['davg'])
dmax = np.interp(t, t2, df_knn['dmax'])

#plt.plot(t, (df_crm['avg'] + avg) / 2, '--', label='Actual faults')
plt.plot(t, df_crm['avg'], '--', label='Actual faults')
plt.fill_between(t, df_crm['min'], df_crm['max'], color='blue', alpha=.15)

plt.plot(t, df_crm['davg'], label='CRM')
plt.fill_between(t, df_crm['dmin'], df_crm['dmax'], color='orange', alpha=.15)

plt.plot(t, davg, ':', label='KNN')
plt.fill_between(t, dmin, dmax, color='grey', alpha=.15)

plt.xlabel('Time (simulation step)')
plt.ylabel('Number of faults')
plt.legend()
plt.show()
