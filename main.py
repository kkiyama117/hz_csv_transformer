# これはサンプルの Python スクリプトです。
import csv
from parser import parse_file_info, parse_messing_info, parse_condition_info, parse_pgs
from parser.slicer import slice_csv_sjis
from utils import convert_to_utf


def open_csv(filename):
    slice_csv_sjis(filename)


# ガター内の緑色のボタンを押すとスクリプトを実行します。
if __name__ == '__main__':
    file_name = "./csv/CV_1.CSV"
    # import polars as pl
    # q = pl.scan_csv(file_name)
    # print(q.columns)
    convert_to_utf(file_name)
    open_csv(file_name)

# test_csv(input)

# PyCharm のヘルプは https://www.jetbrains.com/help/pycharm/ を参照してください
