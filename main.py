import math

from parser import parser
from plotter.cv import create_cv_graph
from utils import convert_to_utf

if __name__ == '__main__':
    file_name = "./csv/CV_3.CSV"
    convert_to_utf(file_name)
    _r = 0.15
    with parser.open_csv(file_name) as parsed_csv:
        area = pow(_r,2)*math.pi
        print(area)
        create_cv_graph(parsed_csv,area)
