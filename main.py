# これはサンプルの Python スクリプトです。
import csv
from parser import parse_file_info, parse_messing_info, parse_condition_info, parse_pgs


def open_csv_sjis(filename):
    with open(filename, newline='', encoding="sjis") as f:
        csv_reader = csv.reader(
            f, delimiter=",", skipinitialspace=True
            # f, delimiter=','
        )
        stream, file_info = parse_file_info(csv_reader)
        print(file_info)
        stream, measure_info = parse_messing_info(csv_reader)
        print(measure_info)
        stream, condition_info = parse_condition_info(csv_reader)
        print(condition_info)
        stream, condition_info = parse_pgs(csv_reader)
        print(condition_info)


def open_csv(filename):
    open_csv_sjis(filename)


# ガター内の緑色のボタンを押すとスクリプトを実行します。
if __name__ == '__main__':
    open_csv('./csv/CV_1.CSV')
    # test_csv(input)

# PyCharm のヘルプは https://www.jetbrains.com/help/pycharm/ を参照してください
