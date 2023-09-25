from typing import Iterator

from models.csv_structure import FileInfo, MeasureInfo
from .models import RowData, BlockData
from .utils import parse_row_data, parse_block


def parse_file_info(str_stream: Iterator):
    first_row: list = next(str_stream)
    if first_row[0] != '《ファイル情報》':
        return str_stream, None
    else:
        # TODO: 行数が変わった際に対応
        second_row: list = next(str_stream)
        if second_row[1] == "測定項目情報":
            koumoku = int(second_row[2], base=16)
            kind = second_row[3]
        else:
            return str_stream, None
        # TODO: 測定タイトル
        third_row: list = next(str_stream)
        fourth_row: list = next(str_stream)
        version = parse_row_data(fourth_row, "解析バージョン", 2, 1)
        fifth_row: list = next(str_stream)
        sector = parse_row_data(fifth_row, "解析フェイズセクション数", 2, 1)
    file_info = FileInfo(koumoku, kind, version, sector)
    return str_stream, file_info


def parse_messing_info(stream: Iterator):
    _data = BlockData(
        title='《測定情報》',
        rows=[
            RowData("siryou", "試料"),
            RowData("working_electrode", "作用極"),
            RowData("area", "面積"),
            RowData("solution", "電解質溶液"),
            RowData("concentration", "濃度"),
            RowData("reference_electrode", "参照電極"),
            RowData("temperature", "温度"),
            RowData("comment", "コメント"),
        ]
    )
    stream, result = parse_block(stream, _data)
    return stream, MeasureInfo(**result)
