import math

from parser import parser
from plotter.cv import create_cv_graph
from utils import convert_to_utf, generate_origin_data

if __name__ == '__main__':
    file_name = "./csv/CV_3.CSV"
    convert_to_utf(file_name)
    # calc your electrode area
    _r = 0.15
    area = pow(_r, 2) * math.pi
    print(area)
    # generate graph
    with parser.open_csv(file_name) as parsed_csv:
        create_cv_graph(parsed_csv, area)
    # get cv_data
    with parser.open_csv(file_name) as parsed_csv:
        for i in generate_origin_data(parsed_csv, area):
            print(i)
