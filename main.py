# これはサンプルの Python スクリプトです。
import csv
from parser import parse_file_info, parse_messing_info, parse_condition_info, parse_pgs
from parser.slicer import slice_csv_sjis
from utils import convert_to_utf


def open_csv(filename):
    slice_csv_sjis(filename)


# ガター内の緑色のボタンを押すとスクリプトを実行します。
if __name__ == '__main__':
    convert_to_utf('./csv/CV_1.CSV')
    open_csv('./csv/CV_1.CSV')
    import polars as pl

    q = pl.scan_csv("./csv/CV_1.CSV")
    print(q.columns)

# test_csv(input)

# PyCharm のヘルプは https://www.jetbrains.com/help/pycharm/ を参照してください
