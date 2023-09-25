from dataclasses import dataclass


@dataclass
class FileInfo:
    koumoku: int
    kind: str
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
