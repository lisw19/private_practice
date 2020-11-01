# -*-@Time: 2020/11/1-*-
import re
import pandas as pd

pwd = "/Users/lishiwei/Desktop/782694_2020_10_30.xlsx"
data = pd.read_excel(pwd)


def scientific_deal(ser):
    c = str(ser['color'])
    t = str(ser['title'])
    if c and c != 'nan':
        return c
    res_title = ' '
    if not t:
        return res_title
    titles = t.strip().split(' ')
    if len(titles) >= 2:
        res_title = re.sub('([\u4e00-\u9fa5]+)', '**', titles[-2])
    elif len(titles) < 2:
        res_title = re.sub('([\u4e00-\u9fa5]+)', '**', titles[-1])
    return res_title


data['goods_code2'] = data.apply(scientific_deal, axis=1)
data.to_excel('/Users/lishiwei/Workspace/private_python/excel_tools/jd_11_01.xlsx', index=False, header=True)
