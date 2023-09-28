from typing import Iterator

from models.csv_structure import FileInfo, MeasureInfo, ConditionInfo, MainMeasureCondition, FirstPotentialCondition, \
    PostProcessingCondition, NaturePotentialCondition, PGSInfo
from .models import RowData, BlockData
from .utils import parse_row_data, parse_block_with_title, parse_block


class NextIterator:
    def __init__(self, stream):
        # *args
        # self.args = args
        self.stream = stream

    def __iter__(self) -> Iterator:
        return self

    def __next__(self):
        _block_title = ""
        _block_title = next(self.stream)[0]
        while _block_title == "":
            _block_title = next(self.stream)[0]
        result = None
        if _block_title == "《ファイル情報》":
            stream, result = parse_file_info(self.stream)
        elif _block_title == '《測定情報》':
            stream, result = parse_messing_info(self.stream)
        elif _block_title == '《測定条件》':
            stream, result = parse_condition_info(self.stream)
        elif _block_title == '《PGS設定》':
            stream, result = parse_pgs(self.stream)
        else:
            raise StopIteration
        return result


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
    if int(result.get("koumoku"), 16) == 1283:
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
    # title = '《測定条件》'
    # while next(stream)[0] != title:
    #     pass
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
    stream, result = parse_block_with_title(stream, _data)
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
    stream, result = parse_block_with_title(stream, _data)
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
    stream, result = parse_block_with_title(stream, _data)
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
    stream, result = parse_block_with_title(stream, _data)
    return stream, PostProcessingCondition(**result)


def parse_pgs(stream):
    first_row: list = next(stream)
    # title = '《PGS設定》'
    # while next(stream)[0] != title:
    #     pass
    _data = BlockData(
        title="[本測定]",
        start=2,
        rows=[
            RowData("operating_mode", "動作モード", start=3, count=2),
            RowData("internal_setting", "内部設定有効選択", start=3),
            RowData("internal_voltage", "内部設定電圧", start=3),
            RowData("internal_currency", "内部設定電流", start=3),
            RowData("external_connection", "外部入力の接続", start=3),
            RowData("voltage_range", "電圧レンジ", start=3),
            RowData("current_range", "電流レンジ", start=3),
            RowData("minimum_current_range", "電流下限レンジ", start=3),
            RowData("current_limit", "電流リミット", start=3),
            RowData("filter", "フィルタ", start=3),
            RowData("response", "レスポンス", start=3),
        ]
    )
    stream, result = parse_block(stream, _data)
    return stream, PGSInfo(**result)

def parse_cvcycle():
    pass