import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ggplot import *
from collections import Counter

%matplotlib inline

def entries_histogram(filename):
    turnstile_weather = pd.read_csv(filename)
    
    plt.figure()
    turnstile_weather.ENTRIESn_hourly[turnstile_weather['rain'] == 0].hist(bins=range(0,6000,250)) 
    turnstile_weather.ENTRIESn_hourly[turnstile_weather['rain'] == 1].hist(bins=range(0,6000,280)) 
    plt.legend(['No Rain','Rain'])
    plt.title("Histogram of Subway Ridership")
    plt.xlabel("Number of hourly entries")
    plt.ylabel("Frequency")
    
    turnstile_weather['DATEn'] = pd.to_datetime(turnstile_weather['DATEn'])
    tw = turnstile_weather.set_index(['DATEn'])
    tw = tw[['Hour','ENTRIESn_hourly']]
    tw['DOW'] = tw.index.weekday
    #print tw.head(20)
    data = tw.groupby(['DOW','Hour']).mean() # mean entries per dow per hour
    print Counter(tw.Hour)
    Matrix = np.array([[data.ENTRIESn_hourly[x,y] for x in range(7)] for y in range(24)])
    
    fig, ax = plt.subplots()
    
    heatmap = ax.pcolor(Matrix, cmap=plt.cm.Blues, alpha=0.8)
    # turn off the frame
    ax.set_frame_on(False)
    # put the major ticks at the middle of each cell
    
    ax.set_xticks(np.arange(Matrix.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    labels = ['Mon','Tues','Wed','Thur','Fri','Sat','Sun']
    ax.set_xticklabels(labels, minor=False)
    ax = plt.gca()
    for t in ax.xaxis.get_major_ticks():
        t.tick1On = False
        t.tick2On = False
    for t in ax.yaxis.get_major_ticks():
        t.tick1On = False
        t.tick2On = False
    ax.set_ylabel("Hour")
    fig.suptitle("Subway Ridership by Day and Hour", fontsize=14, fontweight='bold')
    fig.subplots_adjust(top=0.85)
    
    cbar = plt.colorbar(heatmap, orientation = "horizontal")
    #cbar.ax.set_yticklabels(['0','1','2','>3'])
    cbar.set_label('Number of Entries on Average')
    return plt

entries_histogram('~/Desktop/P2_NYCRidershipData/turnstile_data_master_with_weather.csv')
