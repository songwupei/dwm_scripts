import itertools
from collections import OrderedDict, defaultdict
from pathlib import Path

import polars as pl

from play_text import contains_CJK, split_rPath_names, split_OnePath_names
from play_text import play_csv

from getschema import get_schema
import pdb

FinDataPath = Path("/home/song/NutstoreFiles/8-MyData/FinData/")
schema_filepath = FinDataPath / "Blank/附录.中央企业司库信息资源编目.xlsx"
usedcolumns_dict_index = [2, *list(range(11, 14))]
usedcolumns_dict_index = [i - 1 for i in usedcolumns_dict_index]

csv_paths = Path.cwd().rglob(r"*.csv")
SplitPathNamesCLS = split_rPath_names(csv_paths)
csv_names_CJK_list = SplitPathNamesCLS.get_CJK_list()
csv_names_TABLENAME_set = sorted(
    set(csv_names_CJK_list) - set(["中国兵器工业集团有限公司", "PPP附表"]),
)  ## 上报表名（查找规律包含汉字）
for tablename in csv_names_TABLENAME_set:
    print(tablename)
    if (
        Path("/home/song/Documents/上报国资委司库专班_parquetV2")
        / f"006_中国兵器工业集团有限公司_{tablename}_20200101-20240930.parquet"
    ).exists():
        pass
    else:
        csv_paths_selected_iterator2 = Path.cwd().rglob(f"*{tablename}*.csv")
        PlayCsvCLS = play_csv(csv_paths_selected_iterator2)
        result_df = PlayCsvCLS.get_concatdf()
        # df_schema = get_schema(schema_filepath, usedcolumns_dict_index, tablename)

        # print(df_schema)
        ##        schema_dict = {
        ##            "交易金额": pl.Decimal(precision=15, scale=2),
        ##            "数据日期": pl.Date,
        ##        }
        ##polars.exceptions.InvalidOperationError: conversion from `str` to `datetime[μs]`
        ## failed in column '交易时间' for 2840 out of 2840 values: ["2024-08-06 17:02:12"
        ##, "2024-08-06 17:02:10", … "2024-08-05 19:43:54"]
        ##
        ##You might want to try:
        ##- setting `strict=False` to set values that cannot be converted to `null`
        ##- using `str.strptime`, `str.to_date`, or `str.to_datetime` and providing a form
        ##at string
        # select(
        ##            pl.col("交易时间").str.to_datetime("%Y-%m-%d %H-%M-%S"),
        ##            pl.col("数据日期").str.to_date("%Y-%m-%d"))
        ##        result_df = result_df.select(pl.col("交易时间").str.to_datetime())
        # result_df.cast(schema_dict).sink_parquet(
        result_df.sink_parquet(
            Path("/home/song/Documents/上报国资委司库专班_parquetV2")
            / f"006_中国兵器工业集团有限公司_{tablename}_20200101-20240930.parquet"
        )
pdb.set_trace()
