# encoding: utf-8
import codecs
import pandas as pd
import os
import re


region_mapping = '''
    C,基隆市
    A,臺北市
    F,新北市
    H,桃園縣
    O,新竹市
    J,新竹縣
    K,苗栗縣
    B,臺中市
    M,南投縣
    N,彰化縣
    P,雲林縣
    I,嘉義市
    Q,嘉義縣
    D,臺南市
    E,高雄市
    T,屏東縣
    G,宜蘭縣
    U,花蓮縣
    V,臺東縣
    X,澎湖縣
    W,金門縣
    Z,連江縣
'''.strip().split('\n')
region_mapping = dict([x.strip().split(',') for x in region_mapping])

deal_type_mapping = '''
    A:不動產買賣
    B:預售屋買賣
    C:不動產租賃
'''.strip().split('\n')
deal_type_mapping = dict([x.strip().split(':') for x in deal_type_mapping])


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
                fields = line.strip().split(',')
            else:
                data = parse_line(line, len(fields))
                dataset.append(data)

    if len(dataset) != 0:
        df = pd.DataFrame(dataset, columns=fields)
        df = df.set_index(u'編號')
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
                print fullpath
                df = parse_file(fullpath)
                df['region'] = region_mapping[region]
                df['quarter'] = quarter

                if len(df) > 0:
                    if deal_type not in dataset:
                        dataset[deal_type] = df
                    else:
                        dataset[deal_type] = dataset[deal_type].append(df)

    for deal_type in dataset:
        filename = '%s.pkl' % deal_type_mapping[deal_type]
        print 'write file %s' % filename
        dataset[deal_type].to_pickle(filename)
