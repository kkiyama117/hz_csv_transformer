# これはサンプルの Python スクリプトです。
import csv
from parser import parse_file_info, parse_messing_info, parse_condition_info, parse_pgs, NextIterator
from utils import convert_to_utf
from models.csv_structure import CVData, PhaseInfoKind


def open_csv(filename):
    with open(filename, newline='') as f:
        csv_reader = csv.reader(
            f, delimiter=",", skipinitialspace=True
        )
        result = []
        for i in filter(_is_real_data, NextIterator(csv_reader)):
            print(i)
            # result.append(i)


def _is_real_data(data):
    return type(data) is CVData and data.phase.kind == PhaseInfoKind.real


# ガター内の緑色のボタンを押すとスクリプトを実行します。
if __name__ == '__main__':
    file_name = "./csv/CV_1.CSV"
    convert_to_utf(file_name)
    open_csv(file_name)

# test_csv(input)

# PyCharm のヘルプは https://www.jetbrains.com/help/pycharm/ を参照してください
