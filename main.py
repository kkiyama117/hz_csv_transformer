import math

from hv_csv_transformer.parser.hz7000 import parser
from hv_csv_transformer.plotter.cv import create_cv_graph_all
from hv_csv_transformer.utils import convert_to_utf

if __name__ == '__main__':
    file_name = "./csv/CV_3.CSV"
    convert_to_utf(file_name)
    # calc your electrode area
    _r = 0.15
    # 0.15cm*0.15cm*Pi
    area = pow(_r, 2) * math.pi
    # generate graph
    with parser.open_csv(file_name) as parsed_csv:
        create_cv_graph_all(parsed_csv, area)
    # get cv_data
    # with parser.open_csv(file_name) as parsed_csv:
    #     for i in generate_origin_data(parsed_csv, area):
    #         print(i)
