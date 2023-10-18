import csv
import contextlib
from typing import Iterator

from hv_csv_transformer.models.csv_structure import FileInfo, MeasureInfo, ConditionInfo, MainMeasureCondition, FirstPotentialCondition, \
    PostProcessingCondition, NaturePotentialCondition, PGSInfo, CVPhaseInfo, PhaseInfoKind, CycleInfo, SamplingHeader, \
    CVData, AnalysisDataHeader, CSVInfo
from .models import RowData, BlockData
from .utils import parse_block_with_title, parse_block, original_datetime_converter, csv_table_parser


@contextlib.contextmanager
def open_csv(filename):
    with open(filename, newline='', mode="r") as f:
        csv_reader = csv.reader(
            f, delimiter=",", skipinitialspace=True
        )
        yield NextIterator(csv_reader)


def open_csv2(filename):
    with open(filename, newline='', mode="r") as f:
        csv_reader = csv.reader(
            f, delimiter=",", skipinitialspace=True
        )
        return NextIterator(csv_reader)


class NextIterator:
    def __init__(self, stream: Iterator, ):
        # *args
        # self.args = args
        self.stream = stream

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> CSVInfo:
        # 0. data
        _block_title = ""
        result = None

        # 1. 次の行を取る
        _block_title = next(self.stream)[0]
        # 2. 次が空ならデータ入りに当たるまで取り続ける
        while _block_title == "":
            _block_title = next(self.stream)[0]

        # 3. 場合分けして取る, 未知ならStopIteration
        if _block_title == "《ファイル情報》":
            stream, result = parse_file_info(self.stream)
        elif _block_title == '《測定情報》':
            stream, result = parse_messing_info(self.stream)
        elif _block_title == '《測定条件》':
            stream, result = parse_condition_info(self.stream)
        elif _block_title == '《PGS設定》':
            stream, result = parse_pgs(self.stream)
        elif _block_title == '《測定フェイズヘッダ》':
            stream, result = parse_cv_cycle(self.stream)
        elif _block_title == '《解析データヘッダ》':
            stream, result = parse_analysis_header(self.stream)
        else:
            raise StopIteration
        return result


def parse_file_info(stream: Iterator) -> (Iterator, CSVInfo):
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


def parse_messing_info(stream: Iterator) -> (Iterator, CSVInfo):
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


def parse_condition_info(stream: Iterator) -> (Iterator, CSVInfo):
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


def _parse_honsokutei(stream) -> (Iterator, CSVInfo):
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


def _parse_sizendeni(stream) -> (Iterator, CSVInfo):
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


def _parse_syokideni(stream) -> (Iterator, CSVInfo):
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


def _parse_atosyori(stream) -> (Iterator, CSVInfo):
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


def parse_pgs(stream) -> (Iterator, CSVInfo):
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


def _parse_phase_info(stream) -> (Iterator, CSVInfo):
    _data = BlockData(
        title='《測定ファイルヘッダ》',
        rows=[
            RowData("_phase_int", "フェイズ情報"),
            RowData("cycle_num", "サイクル番号"),
            RowData("measure_point", "測定点数"),
        ]
    )
    stream, result = parse_block(stream, _data)
    _phase_int = result.pop("_phase_int")
    if int(_phase_int, 16) == 1537:
        result["kind"] = PhaseInfoKind.natural
    elif int(_phase_int, 16) == 1538:
        result["kind"] = PhaseInfoKind.first
    elif int(_phase_int, 16) == 1536:
        result["kind"] = PhaseInfoKind.real
    else:
        result["kind"] = PhaseInfoKind.unknown

    return stream, CVPhaseInfo(**result)


def _parse_cycle_info(stream) -> (Iterator, CSVInfo):
    # title = '《PGS設定》'
    # while next(stream)[0] != title:
    #     pass
    _data = BlockData(
        title='《サイクル情報》',
        rows=[
            RowData("start", "開始時間"),
            RowData("end", "終了時間"),
        ]
    )
    stream, result = parse_block_with_title(stream, _data)
    result["start"] = original_datetime_converter(result["start"])
    result["end"] = original_datetime_converter(result["end"])
    return stream, CycleInfo(**result)


def _parse_sampling_header(stream) -> (Iterator, CSVInfo):
    _data = BlockData(
        title='《測定サンプリングヘッダ》',
        rows=[
            RowData("data_count", "データ数"),
            RowData("item_count", "データ項目数"),
        ]
    )
    stream, result = parse_block_with_title(stream, _data)
    return stream, SamplingHeader(**result)


def parse_cv_cycle(stream) -> (Iterator, CVData):
    base = {}
    # title = '《測定フェイズヘッダ》'
    # while next(stream)[0] != title:
    #     pass
    stream, result = _parse_phase_info(stream)
    base["phase"] = result
    stream, result = _parse_cycle_info(stream)
    base["info"] = result
    stream, result = _parse_sampling_header(stream)
    base["header"] = result
    stream, result = csv_table_parser(stream)
    base["data"] = result
    return stream, CVData(**base)


def parse_analysis_header(stream) -> (Iterator, CSVInfo):
    _data = BlockData(
        title='《解析データヘッダ》',
        rows=[
            RowData("data_count", "解析データ数"),
        ]
    )
    stream, result = parse_block(stream, _data)
    return stream, AnalysisDataHeader(**result)
