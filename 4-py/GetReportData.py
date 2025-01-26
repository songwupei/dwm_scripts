#!/bin/python3

import re
from collections import defaultdict
#ReportPath = '/home/song/NutstoreFiles/8-MyData/report/2024年1-11月经济运行动态信息情况-refine.txt'
def ProcessFile(PatternItem, SourcePath):
    RePattern = f"{PatternItem}(为|的|共|（)?(?P<{PatternItem}>(\d*\.?\d*(个|亿元|万元|%|万笔|家|笔))(（\d*\.?\d*(个|亿元|万元|%|万笔|家|笔)）)?)"
    with open(SourcePath,'r') as file:
        text=file.read()
        file.close()
    try:
        groupdict = re.search(RePattern,text).groupdict()
    except Exception as e:
        print(f'An error about {PatternItem} raise:{e}!')
        groupdict = {PatternItem:"NoData"}


    month = re.match('\d+年\d+月',text).group()
    return month, groupdict

def GetFormatData(NormalPath, SourcePath):

    with open(NormalPath,'r') as file:
        normaltext = file.read()
        file.close()
    items_list=normaltext.split()

    # ReportDataDict=defaultdict(list)
    ReportDataDict={}
    #for month in month_list:text
    MonthDataDict={}
    for item in items_list:
        month, DataDict = ProcessFile(item, SourcePath)
        MonthDataDict.update(DataDict)
    ReportDataDict[month] = MonthDataDict
    return ReportDataDict

NormalPath = r'./report_normal.txt'
month_list=[f'2024年{m}月' for m in range(1,12)]
#ReportDataDict = defaultdict(list)
ReportDataDict = {}
for month in month_list:
    ReportPath = f'./2024年经济运行动态情况/{month}经济运行动态信息情况.txt'
    ReportDataDict.update(GetFormatData(NormalPath, ReportPath))
import json


with open('./ReportData.json', 'w+') as file:
    file.write(json.dumps(ReportDataDict))
    file.close()
import polars as pl
import pandas as pd
from tabulate import tabulate
dfs_dict = defaultdict(pl.DataFrame)
dbconnection = "sqlite:///./ReportData.db"
for k,v in ReportDataDict.items():
    dfs_dict[k] = (pl.
                   from_dict(v).
                   with_columns(

        数据年月 = pl.lit(k))
    )
concat_df = pl.concat(dfs_dict.values())
markdown_table = tabulate(concat_df.transpose(), headers=concat_df.columns, tablefmt='github')
#print(concat_df)
#dfs_dict[k].write_database(k, dbconnection, if_table_exists='replace')
#print(dfs_dict)
concat_df.write_csv('./reportdata.csv')

print(markdown_table)
with open('my_table.md', 'w') as f:
    f.write(markdown_table)
##import duckdb

##con = duckdb.connect('./ReportData.db')
##print(con.sql("select * From '2024年1月'"))
