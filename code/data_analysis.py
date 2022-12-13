import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import json
from collections import defaultdict

movies_data = pd.read_csv("./movies.csv")

def analysis_rq1():
    '''
        Distribution of runtime
    '''
    dataDict = {
        "0-60 min": 0,
        "60-120 min": 0,
        "120-180 min": 0,
        "180+ min": 0
    }
    movies_data.dropna(axis = 0,subset = ["Runtime"],inplace=True)
    for item in movies_data["Runtime"]:
        if item == "Runtime":
            continue
        item = str(item)
        time = int(item.split(' ')[0])
        if time<=60:
            dataDict["0-60 min"] += 1
        elif time > 60 and time <= 120:
            dataDict["60-120 min"] += 1
        elif time > 120 and time <= 180:
            dataDict["120-180 min"] += 1
        elif time > 180:
            dataDict["180+ min"] += 1
        else:
            print(">>runtime error!")
            print(item)

    return dataDict
    

def plot_rq1(data:dict,savename):
    print(data)
    x = list(data.values())
    label = list(data.keys())
    color = plt.get_cmap('BuPu')(np.linspace(0.2, 0.7, len(data)))
    explode = (0.1,0,0,0)
    fig,ax = plt.subplots()
    ax.pie(x,labels = label,colors = color,explode = explode,shadow = True,startangle=90,autopct='%1.1f%%')
    ax.axis('equal')
    ax.set_title('Distribution of runtime',pad=20,fontweight='bold',fontsize = 15)
    plt.savefig(savename)

def analysis_rq2():
    '''
        Top genres data
    '''
    dataDict = defaultdict(int)
    for item in movies_data["Genres"]:
        # print(item)
        for genre in item.split(r','):
            dataDict[genre.strip()] += 1
    temp = {}
    for item in sorted(dataDict.items(),key=lambda item:item[1],reverse=False):
        temp[item[0]] = item[1]
    return temp


def plot_rq2(data:dict,savename):
    genres = list(data.keys())
    count = list(data.values())
    print(len(genres))
    colors = plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85, len(genres)))
    fig,ax = plt.subplots()
    ax.set_ylabel('Genres')
    ax.set_xlabel('Count')
    ax.set_title('Top Genres')
    rects = ax.barh(genres,count,color = colors,height = 0.8)
    ax.bar_label(rects,label_type='edge')
    plt.savefig(savename)

def analysis_rq3():
    '''
        Distribution of ratings
    '''
    ratings = []
    movies_data.dropna(axis = 0,subset = ["Ratings"],inplace=True)
    for item in movies_data["Ratings"]:
        if item == "Ratings":
            continue
        ratings.append(float(item))
    return ratings

def plot_rq3(data:dict,savename):
    plt.figure(figsize = (6, 4))
    plt.hist(data, bins=60, density = False)
    plt.xlabel("Ratings")
    plt.ylabel("Count")
    plt.title("Histogram of Ratings")
    plt.savefig(savename)

import IPython
def processYeardata(item):
    years = []
    year = []
    item = str(item)
    for i in range(len(item)):
        if item[i].isdigit():
            year.append(item[i])
    if year == []:
        return None
    elif len(year) > 4:
        years.append(int("".join(year[:4])))
        years.append(int("".join(year[4:])))
    else:
        years.append(int("".join(year)))

    return years

def analysis_rq4():
    data = {}
    genres = analysis_rq2()
    data["genres"] = list(genres.keys())
    
    years = []
    df = movies_data.dropna(axis = 0,subset = ["Year"],inplace=False)
    for item in df["Year"]:
        val = processYeardata(item)
        if not val:
            continue
        else:
            years.extend(val)
    years = sorted(set(years))
    data["years"] = years

    genres_data = {}
    for genre in list(genres.keys()):
        genres_data[genre] = defaultdict(int)
    for _,row in df.iterrows():
        item = row["Genres"]
        year = processYeardata(row["Year"])
        if not year:
            continue
        for genre in item.split(r','):
            for i in range(len(year)):
                genres_data[genre.strip()][year[i]] += 1
    data["raw_data"] = genres_data

    htmldata = []
    for k,v in genres_data.items():
        temp = []
        for y in years:
            if y in v.keys():
                temp.append(v[y])
            else:
                temp.append(0)
        counts = np.cumsum(temp,axis=0).tolist()

        
        for i in range(len(years)):
            item = []
            item.append(counts[i])
            item.append(k)
            item.append(years[i])
            htmldata.append(item)
    data["data"] = htmldata

    return data



if __name__ == '__main__':

    # data_rq1 = analysis_rq1()
    # plot_rq1(data_rq1, "/result/rq1.pdf")

    # data_rq2 = analysis_rq2()
    # plot_rq2(data_rq2, "/result/rq2.pdf")

    # data_rq3 = analysis_rq3()
    # plot_rq3(data_rq3, "/result/rq3.pdf")

    # save interactive bar growth data
    data_rq4 = analysis_rq4()
    with open("/result/liveBar.json",'w',encoding='utf-8') as fp:
        json.dump(data_rq4, fp,indent=4)

