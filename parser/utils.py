from typing import Iterator, List

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
