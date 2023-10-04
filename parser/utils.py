from typing import Iterator, List
import datetime
import zoneinfo
import maya
import polars as pl

from .models import BlockData, RowData


# data_info を基にstreamからデータを取得してdictとして返す
# streamは部分的に消費していくのでこれも返す
# TODO: 行数が変わった際に対応
def parse_block_with_title(stream: Iterator, data_info: BlockData):
    title = data_info.title
    while next(stream)[data_info.start - 1] != title:
        pass
    return parse_block(stream, data_info)


def parse_block(stream: Iterator, data_info: BlockData):
    data_list: List[RowData] = data_info.rows
    result = {}
    for _d in data_list:
        row: list = next(stream)
        _data = _parse_row_data_from_rowdata(row, _d)
        result[_d.title] = _data
    return stream, result


def _parse_row_data_from_rowdata(row: List[str], rowdata: RowData):
    return parse_row_data(row, rowdata.japanese, rowdata.start, rowdata.count)


def parse_row_data(row, title, first, count):
    if row[first - 1] == title:
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


def original_datetime_converter(data):
    _format = "%Y/%m/%d %H:%M"
    result = datetime.datetime.strptime(data, _format).replace(tzinfo=zoneinfo.ZoneInfo(key="Asia/Tokyo"))
    result = maya.MayaDT.from_datetime(result)
    return result


def csv_table_parser(stream):
    while next(stream)[0] != "《測定データ》":
        pass
    result = []
    _tmp = []
    # データは2列目から(と信じて取り続ける)
    # 最初だけ列
    _first_row = next(stream)
    for i, data in enumerate(_first_row):
        if data == "":
            _first_row[i] = "NoData" + str(i)
    print(_first_row)
    while True:
        _row_data = next(stream)
        if _row_data[1] == "":
            break
        else:
            _tmp.append(_row_data)
    result = pl.DataFrame(_tmp).transpose()
    result.columns = _first_row
    # result = CVRealData(data=result)
    # print(q.columns)
    return stream, result
