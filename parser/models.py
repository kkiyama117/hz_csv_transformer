from dataclasses import dataclass
from typing import List


@dataclass
class RowData:
    title: str
    japanese: str
    start: int = 2
    count: int = 1


@dataclass
class BlockData:
    title: str
    rows: List[RowData]

