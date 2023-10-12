# これはサンプルの Python スクリプトです。
import csv

from models.csv_structure import CVData
from my_polars import CVTransformer
from parser import NextIterator, is_real_data
from parser import parser
from utils import convert_to_utf


def create_cv_graph(filename, area: float):
    with parser.open_csv(filename) as _iter:
        for data in filter(is_real_data, _iter):
            _trans = CVTransformer(data)
            print(_trans.calc_density(area))
        # result.append(i)


# ガター内の緑色のボタンを押すとスクリプトを実行します。
if __name__ == '__main__':
    file_name = "./csv/CV_1.CSV"
    convert_to_utf(file_name)
    create_cv_graph(file_name, 1)

# test_csv(input)

# PyCharm のヘルプは https://www.jetbrains.com/help/pycharm/ を参照してください
