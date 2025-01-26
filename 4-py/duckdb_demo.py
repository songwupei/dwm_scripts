#!/bin/python3

from mylogger import MyLogger
import sys
from pathlib import Path
from collections import defaultdict
import duckdb
from mylogger import log
@log
def getdbinfo(datadb_pathstr,logger):
    ## 安装插件
    con = duckdb.connect()
    con.install_extension("sqlite")
    con.install_extension("parquet")
    tableAndColnames = defaultdict(list)
    tablerows = defaultdict(list)
    match Path(datadb_pathstr).suffix:
        case ".db":
            con = duckdb.connect(datadb_pathstr)
            # con.sql('alter table BANKINFO rename to BankBasicInfo;')
            bankinfodb_tablesnames_fetchall = con.sql("show tables;").fetchall()
            bankinfodb_tablesnames_list = list(
                i[0] for i in bankinfodb_tablesnames_fetchall
            )
            print(bankinfodb_tablesnames_list)
            for tbname in bankinfodb_tablesnames_list:
                tableAndColnames[tbname] = [
                    i[0]
                    for i in con.sql(
                        f"SELECT column_name FROM duckdb_columns() where table_name = '{tbname}';"
                    ).fetchall()
                ]

            limitedlines = 2
            for tbname in bankinfodb_tablesnames_list:
                tablerows[tbname] = con.sql(f"SELECT * FROM '{tbname}' Limit {limitedlines};"
                    ).fetchall()
##                tablerows[tbname] = [
##                    r
##                    for r in con.sql(
##                        f"SELECT * FROM {tbname} Limit {limitedlines};"
##                    ).fetchall()
##                ]
                print(tbname)
                print(tableAndColnames[tbname])
                print(tablerows[tbname])
            


getdbinfo(sys.argv[1],MyLogger)



