"""PARSER from original CSV file to RAW data structure.
"""
from hv_csv_transformer.parser.hz7000.parser import NextIterator
from hv_csv_transformer.parser.hz7000.utils import is_real_data

# from .models import *

__all__ = [NextIterator, is_real_data]
