from my_polars import CVTransformer
from parser import is_real_data, NextIterator


def create_cv_graph(parsed_csv:NextIterator, area: float):
    for data in filter(is_real_data, parsed_csv):
        _trans = CVTransformer(data)
        print(_trans.calc_density(area))
    # result.append(i)
