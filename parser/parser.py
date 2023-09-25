from typing import Iterator

from models.csv_structure import FileInfo, MeasureInfo
from .models import RowData, BlockData
from .utils import parse_row_data, parse_block


def parse_file_info(stream: Iterator):
    _data = BlockData(
        title='《ファイル情報》',
        rows=[
            RowData("koumoku", "測定項目情報"),
            RowData("title", "測定タイトル"),
            RowData("version", "解析バージョン"),
            RowData("sector", "解析フェイズセクション数"),
        ]
    )
    stream, result = parse_block(stream, _data)
    if result.get("koumoku") == 1283:
        result["kind"] = "CV ｻｲｸﾘｯｸﾎﾞﾙﾀﾝﾒﾄﾘ"
    else:
        result["kind"] = "unknown"

    return stream, FileInfo(**result)


def parse_messing_info(stream: Iterator):
    _data = BlockData(
        title='《測定情報》',
        rows=[
            RowData("siryou", "試料"),
            RowData("working_electrode", "作用極"),
            RowData("area", "面積", count=2),
            RowData("solution", "電解質溶液"),
            RowData("concentration", "濃度", count=2),
            RowData("reference_electrode", "参照電極"),
            RowData("temperature", "温度", count=2),
            RowData("comment", "コメント"),
        ]
    )
    stream, result = parse_block(stream, _data)
    return stream, MeasureInfo(**result)


def parse_condition(stream):
    return stream, None


def _parse_honsokutei(stream):
    return stream, None


def _parse_sizendeni(stream):
    return stream, None


def _parse_syokideni(stream):
    return stream, None


def _parse_atosyori(stream):
    return stream, None
