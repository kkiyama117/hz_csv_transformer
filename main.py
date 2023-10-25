import math
from pathlib import Path

from hv_csv_transformer.parser import parser
from hv_csv_transformer.plotter.cv import create_cv_graph_all
from hv_csv_transformer.utils import convert_to_utf
from hv_csv_transformer import sum_as_string, ExampleClass, PythonClass

if __name__ == '__main__':
    file_name = "csv/CV_3.CSV"
    convert_to_utf(file_name)
    # calc your electrode area
    _r = 0.15
    # 0.15cm*0.15cm*Pi
    area = pow(_r, 2) * math.pi
    # generate graph
    with parser.open_csv(file_name) as parsed_csv:
        create_cv_graph_all(parsed_csv, area, path=Path("~/documents").expanduser())
    print(
        sum_as_string(2, 2)
    )
    # get cv_data
    # with parser.open_csv(file_name) as parsed_csv:
    #     for i in generate_origin_data(parsed_csv, area):
    #         print(i)

    py_class = PythonClass(value=10)
    print(py_class.value)
    exa = ExampleClass(value=11)
    print(exa.value)
    import hv_csv_transformer

    print(
        hv_csv_transformer.__doc__
    )
