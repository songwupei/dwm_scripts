from pathlib import Path

from pd_io_excel import xlsxs_to_csv

source_path = "./中国兵器工业集团有限公司-司库上报数据-20230430/"
dest_path = "./中国兵器工业集团有限公司-20230430/"
filepaths = Path(source_path).rglob("*.xlsx")
xlsxs_to_csv(
    filepaths,
    source_dirpath=source_path,
    dest_dirpath=dest_path,
)
