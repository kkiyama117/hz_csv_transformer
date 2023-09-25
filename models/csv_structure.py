from dataclasses import dataclass


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
    cicles: int
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
    siryou: str
    working_electrode: str
    area: str
    solution: str
    concentration: str
    reference_electrode: str
    temperature: str
    comment: str
