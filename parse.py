# encoding: utf-8
import codecs
import pandas as pd
import os
import re


region_mapping = '''
    C,keelung
    A,taipei_city
    F,new_taipei_city
    H,taoyuan
    O,hsinchu_city
    J,hsinchu_county
    K,miaoli
    B,taichung_city
    M,nantou
    N,changhua
    P,yunlin
    I,chiayi_city
    Q,chiayi_county
    D,tainan_city
    E,kaohsiung_city
    T,pingtung
    G,yilan
    U,hualian
    V,taitung
    X,penghu
    W,kinmen
    Z,lianjiang
'''.strip().split('\n')
region_mapping = dict([x.strip().split(',') for x in region_mapping])

deal_type_mapping = '''
    A:real_estate_trade
    B:presold_house_trade
    C:real_estate_rental
'''.strip().split('\n')
deal_type_mapping = dict([x.strip().split(':') for x in deal_type_mapping])

column_mapping = {
    u'鄉鎮市區': 'zone',
    u'交易標的': 'trade_object',
    u'租賃標的': 'rental_object',
    u'土地區段位置或建物區門牌': 'address',
    u'土地移轉總面積平方公尺': 'transferred_land_size',
    u'租賃總面積平方公尺': 'rental_size',
    u'都市土地使用分區': 'city_estate_type',
    u'非都市土地使用分區': 'country_estate_type',
    u'非都市土地使用編定': 'country_estate_use',
    u'交易年月日': 'trade_time',
    u'租賃年月日': 'rental_time',
    u'交易筆棟數': 'trade_building_count',
    u'租賃筆棟數': 'rental_building_count',
    u'移轉層次': 'n_transferred_floor',
    u'租賃層次': 'n_rental_floor',
    u'總樓層數': 'n_floor',
    u'建物型態': 'building_type',
    u'主要用途': 'main_usage',
    u'主要建材': 'main_material',
    u'建築完成年月': 'built_time',
    u'建物移轉總面積平方公尺': 'transferred_building_size',
    u'租賃總面積平方公尺': 'rental_size',
    u'建物現況格局-房': 'n_bedroom',
    u'建物現況格局-廳': 'n_living_room',
    u'建物現況格局-衛': 'n_bathroom',
    u'建物現況格局-隔間': 'has_partition',
    u'有無管理組織': 'has_admin',
    u'有無附傢俱': 'has_furniture',
    u'總價元': 'trade_price',
    u'總額元': 'rental_price',
    u'單價每平方公尺': 'price_per_m2',
    u'車位類別': 'parking_type',
    u'車位移轉總面積平方公尺': 'parking_size',
    u'租賃總面積平方公尺': 'rental_size',
    u'車位總價元': 'parking_price',
    u'租金總額元': 'another_rental_price',
    u'備註': 'remark',
    u'編號': 'index'
}


def parse_line(line, nrows):
    tmp_data = line.strip().split(',', nrows-2)
    post_data = tmp_data[-1].rsplit(',', 1)
    data = tmp_data[:-1] + post_data
    return data


def parse_file(filename):
    nrow = 0
    dataset = []
    with codecs.open(filename, encoding='cp950', errors='ignore') as f:
        for line in f:
            nrow += 1
            if nrow == 1:
                columns = line.strip().split(',')
                columns = [column_mapping[x] for x in columns]
            else:
                data = parse_line(line, len(columns))
                dataset.append(data)

    if len(dataset) != 0:
        df = pd.DataFrame(dataset, columns=columns)
    else:
        df = pd.DataFrame()

    return df


def check_file(fullpath):
    groups = re.compile('(\w)_lvr_land_(\w).TXT').search(fullpath)
    quarter = fullpath.split('/')[-2]
    if groups is not None:
        assert groups.group(1) in region_mapping
        assert groups.group(2) in deal_type_mapping
        return True, quarter, groups.group(1), groups.group(2)
    return False, '', '', ''


if __name__ == '__main__':
    for deal_type in deal_type_mapping:
        filename = '%s.csv' % deal_type_mapping[deal_type]
        if os.path.exists(filename):
            os.remove(filename)

    org_folder = 'data/'
    dataset = dict()
    for dirpath, _, filenames in os.walk(org_folder):
        for filename in filenames:
            fullpath = os.path.join(dirpath, filename)
            is_valid, quarter, region, deal_type = check_file(fullpath)
            if is_valid:
                print(fullpath)
                df = parse_file(fullpath)
                df['region'] = region_mapping[region]
                df['quarter'] = quarter

                if len(df) > 0:
                    if deal_type not in dataset:
                        dataset[deal_type] = df
                    else:
                        dataset[deal_type] = dataset[deal_type].append(df)

    filename = 'real_estate.h5'
    for deal_type in dataset:
        df = dataset[deal_type].reset_index(drop=True)
        if 'rental_size' in df.columns:
            rental_size = df.rental_size.max(axis=1)
            df = df.drop('rental_size', 1)
            df['rental_size'] = rental_size
        df.to_hdf(filename, key=deal_type_mapping[deal_type])
