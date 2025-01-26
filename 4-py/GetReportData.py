#!/bin/python3

import re
from shutil import copy as cp
from pathlib import Path
from collections import defaultdict

import pandas as pd

import polars as pl
import polars.selectors as cs
from tabulate import tabulate


def ProcessFile(PatternItem, SourcePath):
    PatternItem_Name = re.sub(r'(\w+)盈利\|\S+',r'\1盈亏',PatternItem)
    RePattern = f"({PatternItem})(提示)?(\*\*)?(\[\[\d+\]\]\(#footnote\-\d+\))?(\*\*)?(提示)?(为|的|共|（|\()?(?P<{PatternItem_Name}>(\-?\d*，?,?\.?\d*(个|亿元|万元|%|万笔|家|笔))((\(|（)\d*,?，?\.?\d*(个|亿元|万元|%|万笔|家|笔)(）|\)))?)"
    
    with open(SourcePath,'r') as file:
        text=file.read()
        file.close()
    try:
        text = text.replace("亏损","亏损-")
        text = text.replace("盈亏对冲","盈亏对冲──")
        groupdict = re.search(RePattern,text).groupdict()
    except Exception as e:
        print(f'An error about {PatternItem_Name} raise:{e}!')
        groupdict = {PatternItem_Name:"NoData"}

    month = re.search('\d+年\d+月',text).group()
    return month, groupdict

def GetFormatData(NormalPath, SourcePath):
    with open(NormalPath, 'r') as file:
        normaltext = file.read()
    items_list = [token.replace(" ","|") for token in normaltext.splitlines()]
    ReportDataDict = {}
    MonthDataDict = {}
    for item in items_list:
        month, DataDict = ProcessFile(item, SourcePath)
        MonthDataDict.update(DataDict)
        ReportDataDict[month] = MonthDataDict
    return ReportDataDict

def save_markdown_tables(concat_df, output_dir, cols_default=6):
    num_columns = len(concat_df.columns)-1
    output_normal = './config/output_normal.md'
    file_path = f"{output_dir}/table_output.md"
    if Path(output_normal).exists():
        cp(output_normal, file_path)

    for i in range(0, num_columns, cols_default):
        end = min(i + cols_default, num_columns)
        subset_df = concat_df.select(cs.by_index(-1,range(i,end)))
        headers = subset_df.columns
        colalign = ["center"] +['decimal']*(end -i)
        markdown_table = tabulate(subset_df.transpose(), headers, tablefmt='github',colalign=colalign)
        with open(file_path, 'a') as file:
            file.write(markdown_table)
            file.write('\n')
            file.write('\n')

def clean_numerical_data(df):
    # Split the specified columns based on the delimiter "(（"
    split_columns = ["与系统外单位发生结算交易", "系统结算支出"]
    for col in split_columns:
        if col in df.columns:
            # Split the column into two parts based on the delimiter "(（"
            df = df.with_columns(
                pl.col(col)
                .str.replace_all(r'[\(（]', '（')
                .str.replace_all(r'[\)）]', '')
                .str.split_exact("（", 1)
                .struct.rename_fields([f"{col}_金额", f"{col}_笔数"])
                .alias("fields")
            ).unnest("fields")

            # Reorder columns to place the new columns after the original column
            columns = df.columns
            original_col_index = columns.index(col)
            new_columns = columns[:original_col_index + 1] + [f"{col}_金额", f"{col}_笔数"] + columns[original_col_index + 1:-2]
            df = df.select(new_columns)
    
            # Drop the original column
            df = df.drop(col)
    
    # Process the remaining columns
    for col in df.columns:
        if col == "数据年月":
            continue
        
        # Extract non-numeric information from the column
        non_numeric_info = (
            df[col]
            .str.extract_all(r'[^\d\.\-]+')
            .explode()
            .unique()
            .drop_nulls()
        )
        
        # Filter out ", " and "NoData" from non_numeric_info
        non_numeric_info = non_numeric_info.filter(
            ~non_numeric_info.is_in([", ", "NoData", ","])
        )
        
        # Combine unique non-numeric information into a single string
        suffix = "（" + ",".join(non_numeric_info.to_list()) + "）" if not non_numeric_info.is_empty() else ""
        
        # Append the suffix to the column name
        new_col_name = col + suffix
        df = df.rename({col: new_col_name})
        
        # Remove commas (,) and full-width commas (，) from the column values
        df = df.with_columns(
            pl.col(new_col_name)
            .str.replace_all(r'[\,，]', '')
            .str.extract(r'(\-?\d*\.?\d+)')
            .cast(pl.Float64)
            .alias(new_col_name)
        )
         
    return df
def round_str(col:str , n:int):
    return (
        pl.col(col).round(n).cast(str) + pl.lit("0"*n)
    ).str.replace(rf"^(\-?\d+\.\d{{{n}}}).*$","$1").alias(col)
    


ReNormalPath = r'./config/report_normal.txt'
OutputPath = r'./config/output_normal.md'
ReportDataDict = {}
import glob
ReportPaths_txt = list(glob.glob('./2024年经济运行动态情况/*.txt'))
ReportPaths_md = list(glob.glob('./2024年经济运行动态情况/*.md'))
ReportPaths= ReportPaths_txt+ReportPaths_md
for ReportPath in ReportPaths:
    ReportDataDict.update(GetFormatData(ReNormalPath, ReportPath))

import json

with open('./ReportData.json', 'w+') as file:
    file.write(json.dumps(ReportDataDict))
    file.close()

dfs_dict = defaultdict(pd.DataFrame)
dbconnection = "sqlite:///./ReportData.db"
for k,v in ReportDataDict.items():
    df = pl.from_dict(v)
    df = df.with_columns((pl.lit(k)).alias('数据年月'))
    dfs_dict[k] = df
concat_df = (pl.concat(dfs_dict.values())
             .sort(pl.col('数据年月')
             .str.slice(5)
             .str.strip_suffix("月")
             .cast(pl.Int8))
             )

concat_df = clean_numerical_data(concat_df)
print(concat_df.head())
concat_df.write_csv('./reportdata.csv')
save_markdown_tables(concat_df,'./')
