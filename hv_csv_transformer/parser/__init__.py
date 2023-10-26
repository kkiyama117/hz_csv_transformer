"""PARSER from original CSV file to RAW data structure.
"""
from .parser import NextIterator

try:
    from hv_csv_transformer.hv_csv_transformer.parser import RawData2
except ImportError:
    class RawData2:
        pass

from .utils import is_real_data

# from .models import *

__all__ = [NextIterator, is_real_data]
