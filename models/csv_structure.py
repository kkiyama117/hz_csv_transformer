from dataclasses import dataclass, asdict
import pickle


def info_to_csv(info):
    data_dict = asdict(info)
    with open("test.pickle", mode="wb") as f:
        pickle.dump(info, f)
    pickle_to_info("")


def pickle_to_info(name):
    with open("test.pickle", mode="rb") as f:
        res = pickle.load(f)
    print(res)


@dataclass
class FileInfo:
    koumoku: int
    kind: str
    title: str
    version: int
    sector: int


@dataclass
class MeasureInfo:
    siryou: str
    working_electrode: str
    area: str
    solution: str
    concentration: str
    reference_electrode: str
    temperature: str
    comment: str


@dataclass
class MainMeasureCondition:
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
class NaturePotentialCondition:
    # sec
    measurement_time: int
    # mV
    detected_variation: int
    # sec
    interval: int


@dataclass
class FirstPotentialCondition:
    # V
    initial: int | str
    # sec
    holding_time: int
    # sec
    interval: int


@dataclass
class PostProcessingCondition:
    kind: str
    # sec
    holding_time: int
    # sec
    interval: int


@dataclass
class ConditionInfo:
    main_measure: MainMeasureCondition
    nature_potential: NaturePotentialCondition
    first_potential: FirstPotentialCondition
    post_process: PostProcessingCondition


@dataclass
class PGSInfo:
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
class AllInfo:
    file: FileInfo
    measure: MeasureInfo
    condition: ConditionInfo
    pgs: PGSInfo
