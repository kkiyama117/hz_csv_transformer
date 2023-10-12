from abc import ABCMeta
from dataclasses import dataclass
from enum import Enum, auto

from maya import MayaDT
from polars import DataFrame


class CSVInfo(metaclass=ABCMeta):
    pass


@dataclass
class FileInfo(CSVInfo):
    koumoku: int
    kind: str
    title: str
    version: int
    sector: int


@dataclass
class MeasureInfo(CSVInfo):
    siryou: str
    working_electrode: str
    area: str
    solution: str
    concentration: str
    reference_electrode: str
    temperature: str
    comment: str


@dataclass
class MainMeasureCondition(CSVInfo):
    first_potential: int
    second_potential: int
    # mV/s
    scan_rate: int
    cycles: int
    # ms
    sampling_rate: int
    upper_limit: int | None
    lower_limit: int | None
    dead_time: int | None


@dataclass
class NaturePotentialCondition(CSVInfo):
    # sec
    measurement_time: int
    # mV
    detected_variation: int
    # sec
    interval: int


@dataclass
class FirstPotentialCondition(CSVInfo):
    # V
    initial: int | str
    # sec
    holding_time: int
    # sec
    interval: int


@dataclass
class PostProcessingCondition(CSVInfo):
    kind: str
    # sec
    holding_time: int
    # sec
    interval: int


@dataclass
class ConditionInfo(CSVInfo):
    main_measure: MainMeasureCondition
    nature_potential: NaturePotentialCondition
    first_potential: FirstPotentialCondition
    post_process: PostProcessingCondition


@dataclass
class PGSInfo(CSVInfo):
    operating_mode: str
    internal_setting: str
    # V
    internal_voltage: int
    # ?
    internal_currency: int
    external_connection: str
    voltage_range: str
    current_range: str
    minimum_current_range: str
    current_limit: str
    filter: str
    response: int


@dataclass
class AllInfo(CSVInfo):
    file: FileInfo
    measure: MeasureInfo
    condition: ConditionInfo
    pgs: PGSInfo


class PhaseInfoKind(Enum):
    unknown = 0
    natural = auto()
    first = auto()
    real = auto()

    def __str__(self):
        if self.name == "real":
            return "本測定"
        elif self.name == "natural":
            return "自然電位測定"
        elif self.name == "first":
            return "初期電位測定"
        elif self.name == "unknown":
            return "不明"
        return "不明"


@dataclass
class CVPhaseInfo(CSVInfo):
    kind: PhaseInfoKind
    cycle_num: int
    measure_point: int


@dataclass
class CycleInfo(CSVInfo):
    start: MayaDT
    end: MayaDT


@dataclass
class SamplingHeader(CSVInfo):
    data_count: int
    item_count: int


@dataclass
class CVData(CSVInfo):
    phase: CVPhaseInfo
    info: CycleInfo
    header: SamplingHeader
    data: DataFrame


@dataclass
class AnalysisDataHeader(CSVInfo):
    data_count: int
