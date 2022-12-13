import requests
import json,os
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from multiprocessing import Pool


# If your local network can directly access the website, you don't need to set the HEADERS and PROXIES.
HEADERS = {'User-Agent': 'Mozilla/5.0 (WindowsNT6.1;Win64;x64) AppleWebKit/537.36(KHTML,likeGecko) Chrome/69.0.3497.100 Safari/537.36'}
PROXIES = {"http": "http://127.0.0.1:1087","https": "127.0.0.1:1087"}
HTML_PARSER = "html.parser"
base_url = "https://www.imdb.com"

def getGenres(url):
    dataSources = {}

    req = requests.get(url,headers=HEADERS,proxies=PROXIES)
    if req.status_code != 200:
        print(">>request failed!")
        return
    soup = bs(req.text,HTML_PARSER)
    divs = soup.find_all('div',attrs={'class':'table-cell primary'})
    # there are 24 genres
    for i in range(24):
        tag = divs[i].find_all('a')
        genreName = tag[0].string
        href = tag[0].get('href')
        dataSources[genreName] = base_url + href

    with open("./sourceURL.json",'w',encoding='utf-8') as f:
        json.dump(dataSources, f,indent=4)

def saveHtml(pageText,fp):
    with open(fp,'w',encoding='utf-8') as f:
        f.write(pageText)

def crawler(genre,url):
    genre = genre.strip()
    print(">>{} start...".format(genre))
    try:
        req = requests.get(url,headers=HEADERS,proxies=PROXIES)
        print(req.status_code)
        soup = bs(req.text,HTML_PARSER)
        html_file = os.path.join("original_data",genre + ".html")
        saveHtml(req.text,html_file)
        datalist = []
        divs = soup.find_all('div',attrs={'class':'lister-item mode-advanced'})
        for i in range(len(divs)):
            dataDict = {
                'Name':"",
                'Year':"",
                'Certificate':"",
                'Runtime':"",
                'Genres':"",
                'Director':"",
                'Stars': "",
                'Ratings':"",
                'Metascore':"",
                'Votes': ""
            }
            subDivs = divs[i].find_all('div',attrs={'class':'lister-item-content'})[0]
            dataDict["Name"] = subDivs.h3.a.string
            dataDict["Year"] = subDivs.find_all('span','lister-item-year text-muted unbold')[0].string.replace(r'(','').replace(r')','')
            try:
                dataDict["Ratings"] = subDivs.find_all('div',attrs={'name':'ir'})[0].get('data-value') 
                dataDict["Metascore"] = subDivs.find_all('div','inline-block ratings-metascore')[0].span.string.strip()
            except IndexError as e:
                print("[ERROR]: no ratings")

            tagP = subDivs.find_all('p')
            for j in range(len(tagP)):
                if j == 0:
                    try:
                        dataDict["Certificate"] = tagP[j].find_all('span','certificate')[0].string
                    except Exception as e:
                        print(e)
                        print("[ERROR]: no certificate")
                    try:
                        dataDict["Runtime"] = tagP[j].find_all('span','runtime')[0].string
                    except Exception as e:
                        print(e)
                        print("[ERROR]: no runtime")
                    try:
                        dataDict["Genres"] = tagP[j].find_all('span','genre')[0].string.strip()
                    except Exception as e:
                        print(e)
                        print("[ERROR]: no genres")
                elif j == 1:
                    continue
                elif j == 2:
                    try:
                        tagA = tagP[j].find_all('a')
                        directors = [a.string for a in tagA]
                        dataDict["Director"] = directors[0]
                        dataDict["Stars"] = ",".join(directors[1:])
                    except Exception as e:
                        print(e)
                        print("[ERROR]: no directors")
                else:
                    try:
                        dataDict["Votes"] = tagP[j].find_all('span',attrs={'name':'nv'})[0].get('data-value')
                    except Exception as e:
                        print(e)
                        print("[ERROR]: no votes")
            print(dataDict)
            datalist.append(dataDict)

        df = pd.DataFrame(datalist,columns=('Name','Year','Certificate','Runtime','Genres','Director','Stars','Ratings','Metascore','Votes'))
        df.to_csv("./data/%s.csv" % genre,index=False)
    except Exception as e:
        print(e)
        raise

def fileMerge(input_dir,output_file):
    for file in os.listdir(input_dir):
        df = pd.read_csv(os.path.join(input_dir,file))
        df.to_csv(output_file,mode = 'a+',index=False)

def main():
    file = open("sourceURL.json",'r',encoding='utf-8')
    srcs = json.load(file)
    file.close()
    print(len(srcs.keys()))
    pool = Pool(8)
    for genre,url in srcs.items():
        pool.apply_async(crawler,args=(genre,url,))
    pool.close()
    pool.join()
    print(">>Subprocess Done!")
    fileMerge("./data/", "./movies.csv")


if __name__ == '__main__':
    
    # genreURL = "https://www.imdb.com/feature/genre/?ref_=nv_ch_gr"
    # getGenres(genreURL)

    # test crawler
    # crawler(" Action ", "https://www.imdb.com/search/title?genres=action&title_type=feature&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=facfbd0c-6f3d-4c05-9348-22eebd58852e&pf_rd_r=VCTZ4NX9C1E11S3GZ1CD&pf_rd_s=center-6&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvpop_1")
    main()

    
