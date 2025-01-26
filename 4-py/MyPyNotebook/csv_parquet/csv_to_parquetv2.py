import itertools
from collections import OrderedDict, defaultdict
from pathlib import Path

import polars as pl

from play_text import contains_CJK, split_rPath_names, split_OnePath_names
from play_text import play_csv

import pdb

##"""
##
##class split_rPath_names(object):
##    """
##    :输入 path迭代器
##    """
##
##    def __init__(self, csv_paths):
##
##        self.csv_paths = csv_paths
##        self._csv_names_list = []
##        self.csv_path_stem = [
##            self._csv_names_list.extend(csv_path.stem.split("_"))
##            for csv_path in self.csv_paths
##        ]
##
##    def get_CJK_list(self):
##        return [
##            csv_name
##            for csv_name in self._csv_names_list
##            if contains_CJK(csv_name).contains_chinese()
##        ]
##
##    def get_ONLYNUM_list(self):
##        return [
##            csv_name
##            for csv_name in self._csv_names_list
##            if csv_name.isdigit() and len(csv_name) > 3
##        ]
##
##
##class split_OnePath_names(object):
##    """
##    :输入 单个path
##    """
##
##    def __init__(self, csv_path):
##
##        self.csv_path = csv_path
##        self._csv_names_list = []
##        self.csv_path_stem = [self._csv_names_list.extend(csv_path.stem.split("_"))]
##
##    def get_CJK_list(self):
##        return [
##            csv_name
##            for csv_name in self._csv_names_list
##            if contains_CJK(csv_name).contains_chinese()
##        ]
##
##    def get_ONLYNUM_list(self):
##        return [
##            csv_name
##            for csv_name in self._csv_names_list
##            if csv_name.isdigit() and len(csv_name) > 3
##        ]
##
##
##class play_csv(object):
##    """
##    :withcolname: 需要补齐的列名称
##    """
##
##    def __init__(self, csvpaths_Sequence):
##
##        (
##            self.__csvpaths_Sequence,
##            self.__csvpaths_Sequence1,
##            self.__csvpaths_Sequence2,
##        ) = itertools.tee(csvpaths_Sequence, 3)
##
##    def get_searchresult(
##        self, csv_schema, selcolnames_list, searchcondition, withcolname
##    ):
##        _dfs_list = []
##        for _csvpath in self.__csvpaths_Sequence:
##            ## 取出csv文件有的列名
##            _csv_schema = OrderedDict()
##            _selcolnames_list = list()
##            for colname in pl.scan_csv(_csvpath, infer_schema_length=1).columns:
##                _csv_schema[colname] = csv_schema[colname]
##                _selcolnames_list.append(colname)
##            _notcolnames_list = list(set(selcolnames_list) - set(_selcolnames_list))
##            _df = (
##                pl.scan_csv(
##                    _csvpath,
##                    schema=_csv_schema,
##                    null_values="无",
##                    infer_schema_length=10000,
##                )
##                .select(_selcolnames_list)
##                .filter(eval(searchcondition))
##                .collect()
##            )
##            """
####                if _notcolnames_list:## 添加with_columns
####                    for nl in _notcolnames_list:
####                        _df = _df.with_columns(pl.Series([None]*_df.height).alias(nl))
##                """
##            if _df.height > 0:
##                _dfs_list.append(_df)
##        if len(_dfs_list) > 0:
##            return pl.concat(_dfs_list, how="diagonal")
##
##    def get_colnames_dict(self):
##        _colnames_dict = defaultdict(list)
##        for _csvpath in self.__csvpaths_Sequence1:
##            SplitPathNamesCLS = split_OnePath_names(_csvpath)
##            __csv_names_ONLYNUM_list = SplitPathNamesCLS.get_ONLYNUM_list()
##            __csv_names_ONLYNUM = __csv_names_ONLYNUM_list[0]
##            _colnames_dict[__csv_names_ONLYNUM] = pl.scan_csv(
##                _csvpath, infer_schema_length=1
##            ).columns
##        return _colnames_dict
##
##    def get_colnames_union(self):
##        import copy
##
##        __colnames_dict = self.get_colnames_dict()
##        __colname_union = []
##        __colname_diff = []
##        for _, v in __colnames_dict.items():
##            __colname_union.extend(v)
##        __colname_diff = list(set(__colname_union) - set(v))  # v是最后一次上报的表
##        __ordered_colnames_list = copy.deepcopy(v)
##        __ordered_colnames_list.extend(__colname_diff)
##        return sorted(list(set(__colname_union)), key=__ordered_colnames_list.index)
##
##    def get_schema_dict(self):
##        """
####        将原始schema类型都改成 pl.Utf8 格式
##        """
##        _schema_dict = defaultdict()
##        for _csvpath in self.__csvpaths_Sequence2:
##            SplitPathNamesCLS = split_OnePath_names(_csvpath)
##            __csv_names_ONLYNUM_list = SplitPathNamesCLS.get_ONLYNUM_list()
##            __csv_names_ONLYNUM = __csv_names_ONLYNUM_list[
##                0
##            ]  ##返回数据日期 如：20240930
##            # 获取每个csv文件的原始schema
##            rawSchema_OrderedDict = pl.scan_csv(_csvpath, infer_schema_length=1).schema
##            # 将原始schema类型都改成 pl.Utf8 格式
##            stringSchema_OrderedDict = OrderedDict()
##            for k, _ in rawSchema_OrderedDict.items():
##                stringSchema_OrderedDict[k] = pl.Utf8
##            _schema_dict[__csv_names_ONLYNUM] = stringSchema_OrderedDict
##        return _schema_dict
##
##    def get_schema_union(self):
##        __schema_dict = self.get_schema_dict()
##        __schema_union = OrderedDict()
##        for _, v in __schema_dict.items():
##            __schema_union.update(v)
##        return __schema_union
##
##    def get_concatdf(self):
##        """
##        :返回df的集合
##        """
##        csv_schema = self.get_schema_union()
##        _dfs_list = []
##        for _csvpath in self.__csvpaths_Sequence:
##            ## 取出csv文件有的列名
##            _csv_schema = OrderedDict()
##            for colname in pl.scan_csv(_csvpath, infer_schema_length=1).columns:
##                _csv_schema[colname] = csv_schema[colname]
##            _df = pl.scan_csv(
##                _csvpath,
##                schema=_csv_schema,
##                infer_schema_length=10000,
##            ).collect()
##
##            if _df.height > 0:
##                _dfs_list.append(_df)
##        if len(_dfs_list) > 0:
##            return pl.concat(_dfs_list, how="diagonal").lazy()

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
        result_df.sink_parquet(
            Path("/home/song/Documents/上报国资委司库专班_parquetV2")
            / f"006_中国兵器工业集团有限公司_{tablename}_20200101-20240930.parquet"
        )
pdb.set_trace()
