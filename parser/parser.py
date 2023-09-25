from typing import Iterator

from models.csv_structure import FileInfo, MeasureInfo, ConditionInfo, MainMeasureCondition, FirstPotentialCondition, \
    PostProcessingCondition, NaturePotentialCondition
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


def parse_condition_info(stream: Iterator):
    base = {}
    first_row: list = next(stream)
    if first_row[0] != "《測定条件》":
        return stream, None
    else:
        stream, result = _parse_honsokutei(stream)
        base["main_measure"] = result
        stream, result = _parse_sizendeni(stream)
        base["nature_potential"] = result
        stream, result = _parse_syokideni(stream)
        base["first_potential"] = result
        stream, result = _parse_atosyori(stream)
        base["post_process"] = result
        return stream, ConditionInfo(**base)


def _parse_honsokutei(stream):
    _data = BlockData(
        title="[本測定]",
        start=2,
        rows=[
            RowData("first_potential", "第1設定電位", start=3),
            RowData("second_potential", "第2設定電位", start=3),
            RowData("scan_rate", "ｽｷｬﾝ速度", start=3),
            RowData("cycles", "ｻｲｸﾙ数", start=3),
            RowData("sampling_rate", "ｻﾝﾌﾟﾘﾝｸﾞ間隔", start=3),
            RowData("upper_limit", "上限ﾘﾐｯﾄﾘﾊﾞｰｽ", start=3),
            RowData("lower_limit", "下限ﾘﾐｯﾄﾘﾊﾞｰｽ", start=3),
            RowData("dead_time", "不感時間", start=3),
        ]
    )
    stream, result = parse_block(stream, _data)
    return stream, MainMeasureCondition(**result)


def _parse_sizendeni(stream):
    _data = BlockData(
        title="[自然電位]",
        start=2,
        rows=[
            RowData("measurement_time", "計測打切時間", start=3),
            RowData("detected_variation", "検出電位変動", start=3),
            RowData("interval", "ｻﾝﾌﾟﾘﾝｸﾞ間隔", start=3),
        ]
    )
    stream, result = parse_block(stream, _data)
    return stream, NaturePotentialCondition(**result)


def _parse_syokideni(stream):
    _data = BlockData(
        title="[初期電位]",
        start=2,
        rows=[
            RowData("initial", "初期電位", start=3),
            RowData("holding_time", "初期電位保持時間", start=3),
            RowData("interval", "ｻﾝﾌﾟﾘﾝｸﾞ間隔", start=3),
        ]
    )
    stream, result = parse_block(stream, _data)
    return stream, FirstPotentialCondition(**result)


def _parse_atosyori(stream):
    _data = BlockData(
        title="[後処理]",
        start=2,
        rows=[
            RowData("kind", "後処理", start=3, count=2),
            RowData("holding_time", "保持時間", start=3),
            RowData("interval", "ｻﾝﾌﾟﾘﾝｸﾞ間隔", start=3),
        ]
    )
    stream, result = parse_block(stream, _data)
    return stream, PostProcessingCondition(**result)
