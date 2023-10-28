from dataclasses import dataclass
from typing import List

try:
    from hv_csv_transformer.hv_csv_transformer import parser_rs

    RowData = parser_rs.models.RowData
    BlockData = parser_rs.models.BlockData
except ImportError as e:
    print(e)
    print("INPORT ERROR")


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
        start: int = 1




__all__ = [RowData, BlockData]
