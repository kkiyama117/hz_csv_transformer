# これはサンプルの Python スクリプトです。
import csv

from models.csv_structure import CVData
from my_polars import CVTransformer
from parser import NextIterator, is_real_data
from utils import convert_to_utf


def open_csv(filename):
    with open(filename, newline='') as f:
        csv_reader = csv.reader(
            f, delimiter=",", skipinitialspace=True
        )
        result = []
        for data in filter(is_real_data, NextIterator(csv_reader)):
            _trans = CVTransformer(data)
            print(_trans.calc_density(1))
            # result.append(i)


# ガター内の緑色のボタンを押すとスクリプトを実行します。
if __name__ == '__main__':
    file_name = "./csv/CV_1.CSV"
    convert_to_utf(file_name)
    open_csv(file_name)

# test_csv(input)

# PyCharm のヘルプは https://www.jetbrains.com/help/pycharm/ を参照してください
