import csv

from models.csv_structure import info_to_csv, AllInfo
from parser import parse_file_info, parse_messing_info, parse_condition_info, parse_pgs, NextIterator


def slice_csv_sjis(filename):
    with open(filename, newline='') as f:
        csv_reader = csv.reader(
            f, delimiter=",", skipinitialspace=True
        )
        for i in NextIterator(csv_reader):
            info_to_csv(i)
        # stream, file_info = parse_file_info(csv_reader)
        # stream, measure_info = parse_messing_info(csv_reader)
        # stream, condition_info = parse_condition_info(csv_reader)
        # stream, pgs_info = parse_pgs(csv_reader)
        # all_info = AllInfo(
        #     file=file_info,
        #     measure=measure_info,
        #     condition=condition_info,
        #     pgs=pgs_info
        # )
        # info_to_csv(all_info)
