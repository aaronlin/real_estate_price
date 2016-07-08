## Description

parser for 內政部不動產成交案件 open data

## Steps:

- download historical data from the link in reference
- unzip the data and put them into folder `data/[quarter]/`
- execute `python parse.py`

## Parsed data:

- format
	- pandas data frame in python pickle file
- data list
	- [不動產租賃](https://s3-ap-northeast-1.amazonaws.com/aaron-public-access/real-estate-price/%E4%B8%8D%E5%8B%95%E7%94%A2%E7%A7%9F%E8%B3%83.pkl)
	- [不動產買賣](https://s3-ap-northeast-1.amazonaws.com/aaron-public-access/real-estate-price/%E4%B8%8D%E5%8B%95%E7%94%A2%E8%B2%B7%E8%B3%A3.pkl)
	- [預售屋買賣](https://s3-ap-northeast-1.amazonaws.com/aaron-public-access/real-estate-price/%E9%A0%90%E5%94%AE%E5%B1%8B%E8%B2%B7%E8%B3%A3.pkl)


## Reference:

- http://plvr.land.moi.gov.tw/DownloadOpenData
