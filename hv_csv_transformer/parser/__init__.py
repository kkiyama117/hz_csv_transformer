"""PARSER from original CSV file to RAW data structure.
"""
from .parser import NextIterator
from .utils import is_real_data

# from .models import *

__all__ = [NextIterator, is_real_data]
