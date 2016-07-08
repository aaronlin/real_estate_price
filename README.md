## Description

parser for 內政部不動產成交案件 open data

## Steps

- download historical data from the link in reference
- unzip the data and put them into folder `data/[quarter]/`
- execute `python parse.py`

## Parsed data

- format
	- pandas data frame in python pickle file
- time range
    - 2012S4 - 2016S3
- data list
	- [不動產租賃](https://s3-ap-northeast-1.amazonaws.com/aaron-public-access/real-estate-price/real_estate_rental.pkl)
	- [不動產買賣](https://s3-ap-northeast-1.amazonaws.com/aaron-public-access/real-estate-price/real_estate_trade.pkla)
	- [預售屋買賣](https://s3-ap-northeast-1.amazonaws.com/aaron-public-access/real-estate-price/presold_house_trade.pkl)


## Translated columns

| original name | translated name |
| ------------- | --------------- |
| 鄉鎮市區 | zone |
| 交易標的 | trade_object |
| 租賃標的 | rental_object |
| 土地區段位置或建物區門牌 | address |
| 土地移轉總面積平方公尺 | transferred_size |
| 租賃總面積平方公尺 | rental_size |
| 都市土地使用分區 | city_estate_type |
| 非都市土地使用分區 | country_estate_type |
| 非都市土地使用編定 | country_estate_use |
| 交易年月日 | trade_time |
| 租賃年月日 | rental_time |
| 交易筆棟數 | trade_building_count |
| 租賃筆棟數 | rental_building_count |
| 移轉層次 | n_transferred_floor |
| 租賃層次 | n_rental_floor |
| 總樓層數 | n_floor |
| 建物型態 | building_type |
| 主要用途 | main_usage |
| 主要建材 | main_material |
| 建築完成年月 | built_time |
| 建物移轉總面積平方公尺 | transferred_size |
| 租賃總面積平方公尺 | rental_size |
| 建物現況格局-房 | n_bedroom |
| 建物現況格局-廳 | n_living_room |
| 建物現況格局-衛 | n_bathroom |
| 建物現況格局-隔間 | has_partition |
| 有無管理組織 | has_admin |
| 有無附傢俱 | has_furniture |
| 總價元 | trade_price |
| 總額元 | rental_price |
| 單價每平方公尺 | price_per_m2 |
| 車位類別 | parking_type |
| 車位移轉總面積平方公尺 | parking_size |
| 租賃總面積平方公尺 | rental_size |
| 車位總價元 | parking_price |
| 租金總額元 | another_rental_price |
| 備註 | remark |
| 編號 | index |


## Reference

- http://plvr.land.moi.gov.tw/DownloadOpenData
