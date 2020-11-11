#!/usr/bin/env python
# coding: utf-8

# In[25]:


import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation


# In[26]:


with open('ms1609025.json') as f:
    data = json.load(f)
    
print ("The data is ", data.keys())


# In[27]:


# data


# In[28]:


# data['moves']


# In[29]:


moves = data['moves']


# In[30]:


# simple code to convert Unixtime into datetime
from datetime import datetime
ts = int("1603701785")

print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))


# In[31]:


len(moves) #show the number of elements in that variable


# In[32]:


# moves[num_move]['StickPositions']


# In[33]:


num_move = 9 # focus to data for each of the moves
StickPositions = pd.DataFrame(moves[num_move]['StickPositions'])
RedDrumPositions = pd.DataFrame(moves[num_move]['RedDrumPositions'])
BlueDrumPositions = pd.DataFrame(moves[num_move]['BlueDrumPositions'])


# In[34]:


BlueDrumPositions.head()


# In[35]:


# split position and time values to better manipulate dataframe

def txtsplit(x):
    return x.split(",")[0], x.split(",")[1], x.split(",")[2]

BlueDrumPositions['x'], BlueDrumPositions['y'], BlueDrumPositions['z'] = zip(*BlueDrumPositions['position'].map(txtsplit))
RedDrumPositions['x'], RedDrumPositions['y'], RedDrumPositions['z'] = zip(*RedDrumPositions['position'].map(txtsplit))
StickPositions['x'], StickPositions['y'], StickPositions['z'] = zip(*StickPositions['position'].map(txtsplit))


# In[36]:


#function to convert Unix time to seconds.milliseconds - easy to plot

def time_correction(df):
    """The first time will be the referrence point till the end of the move"""
    
    df['corr_time'] = df['time'].apply(lambda x : float(x)  - int(df.loc[0,'time'].split(".")[0]))
    
    return df

# function to remove columns which we dont need - position and time. Using x,y,z and corr_time for plots

def clean_df(df):
    """remove the position and old time columns"""
    df.drop(labels = ['position', 'time'], axis=1, inplace=True) ##removes position and time column
    df.sort_values(by=['corr_time'], inplace=True) ##sort the df w.r.t time
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype('float32')
    return df[[ 'corr_time','x', 'y', 'z']]


# In[37]:


time_correction(BlueDrumPositions)


# In[38]:


# dataframe to use the required data

BlueDrumPositions = clean_df(time_correction(BlueDrumPositions))
RedDrumPositions = clean_df(time_correction(RedDrumPositions))
StickPositions = clean_df(time_correction(StickPositions))


# In[39]:


BlueDrumPositions


# In[40]:


StickPositions


# In[41]:


BlueDrumPositions


# In[42]:


RedDrumPositions


# In[43]:


x = StickPositions[["corr_time","x"]].to_numpy()[:,0] ####array
y = StickPositions[["corr_time","x"]].to_numpy()[:,1] ####array

plt.figure(figsize=(10,6))
#plt.axis("off")
plt.yticks(np.arange(y.min(),y.max()))
plt.plot(x,y,"*")


# In[44]:


x = BlueDrumPositions[["corr_time","x"]].to_numpy()[:,0] ####array
y = BlueDrumPositions[["corr_time","x"]].to_numpy()[:,1] ####array


# In[45]:


plt.figure(figsize=(10,6))
#plt.axis("off")
plt.plot(x,y, "-+")


# In[46]:


x = RedDrumPositions[["corr_time","x"]].to_numpy()[:,0] ####array
y = RedDrumPositions[["corr_time","x"]].to_numpy()[:,1] ####array


# In[47]:


plt.figure(figsize=(10,6))
#plt.axis("off")
plt.plot(x,y, "-+")


# In[70]:


# time = StickPositions.to_numpy()[:,0]
# x = StickPositions.to_numpy()[:,1]
# y = StickPositions.to_numpy()[:,2]
# z = StickPositions.to_numpy()[:,3]


# In[78]:


# time = BlueDrumPositions.to_numpy()[:,0]
# x = BlueDrumPositions.to_numpy()[:,1]
# y = BlueDrumPositions.to_numpy()[:,2]
# z = BlueDrumPositions.to_numpy()[:,3]


# In[79]:


time = RedDrumPositions.to_numpy()[:,0]
x = RedDrumPositions.to_numpy()[:,1]
y = RedDrumPositions.to_numpy()[:,2]
z = RedDrumPositions.to_numpy()[:,3]


# In[80]:


fig = plt.figure()
ax = p3.Axes3D(fig) ## create empty 3d axis

# Setting the axes properties
ax.set_xlim3d([-2.0, 2.0])
ax.set_xlabel('X')

ax.set_ylim3d([-2.0,2.0])
ax.set_ylabel('Y')

ax.set_zlim3d([-2.0,4.5])
ax.set_zlabel('Z')

line = ax.plot_wireframe(x.reshape(-1,1) ,y.reshape(-1,1) ,z.reshape(-1,1) )


# In[ ]:





# In[ ]:




