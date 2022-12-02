# 1.Data Description
##Data types
```python
dataDict = {
    'Name':"Black Panther: Wakanda Forever",
    'Year':"2022",
    'Certificate':"PG-13",
    'Runtime':"160 min",
    'Genres':"Action, Adventure, Drama",
    'Director':"Ryan Coogler",
    'Stars': "Letitia Wright,Lupita Nyong'o,Danai Gurira,Winston Duke",
    'Ratings':"7.3",
    'Metascore':"67",
    'Votes': "89766"
}
```
As shown in the example.jpg.
<img src="./example.jpg">

##Data sources
There are a total of 24 movie genres on the website. This project crawled all the movie data of the top 50 in each category and saved them in `movies.csv`.
The `sourceURL.json` contains data sources of 24 categories.
# 2.Code Running 
You can run `crawler.py` with the following commands.
* `python3 crawler.py`
* `nohup python3 crawler.py >./crawler.log 2>&1 &`
# 3.Sample Data Format
Original data in the HTML have been downloaded in the `original_data` directory.