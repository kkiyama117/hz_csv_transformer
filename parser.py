from dataclasses import dataclass
from typing import Iterator, List

from models.csv_structure import FileInfo, MeasureInfo


@dataclass
class RowData:
    title: str
    japanese: str
    start: int = 2
    count: int = 1


@dataclass
class BlockData:
    title: str
    rows: List[RowData]


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
        version = _parse_row_data(fourth_row, "解析バージョン", 2, 1)
        fifth_row: list = next(str_stream)
        sector = _parse_row_data(fifth_row, "解析フェイズセクション数", 2, 1)
    file_info = FileInfo(koumoku, kind, version, sector)
    return str_stream, file_info


def parse_messing_info(stream: Iterator):
    _data = BlockData(
        title='《測定情報》',
        rows=[
            RowData("siryou", "試料"),
            RowData("working_electrode ", "作用極"),
            RowData("area", "面積"),
            RowData("solution ", "電解質溶液"),
            RowData("concentration", "濃度"),
            RowData("reference_electrode ", "参照電極"),
            RowData("temperature ", "温度"),
            RowData("comment ", "コメント"),
        ]
    )
    stream, result = _parse_block(stream, _data)
    print(result)
    return MeasureInfo(**result)


# data_info を基にstreamからデータを取得してdictとして返す
# streamは部分的に消費していくのでこれも返す
# TODO: 行数が変わった際に対応
def _parse_block(stream: Iterator, data_info: BlockData):
    title = data_info.title
    data_list: List[RowData] = data_info.rows
    # pass
    first_row: list = next(stream)
    if first_row[0] != title:
        return stream, None
    else:
        result = {}
        print(data_list)
        for _d in data_list:
            row: list = next(stream)
            print(_d)
            _data = _parse_row_data_from_rowdata(row, _d)
            result[_d.title] = _data
            return stream, result


def _parse_row_data_from_rowdata(row, rowdata: RowData):
    return _parse_row_data(row, rowdata.title, rowdata.start, rowdata.count)


def _parse_row_data(row, title, first, count):
    if row[1] == title:
        if count == 1:
            return row[first]
        elif count > 1:
            data: list = row[first:first + count]
            return "".join(data)
        else:
            # TODO: return Error
            return None
    else:
        # TODO: return Error
        return None
