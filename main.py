from parser import parser
from plotter.cv import create_cv_graph
from utils import convert_to_utf

if __name__ == '__main__':
    file_name = "./csv/CV_1.CSV"
    convert_to_utf(file_name)
    with parser.open_csv(file_name) as parsed_csv:
        create_cv_graph(parsed_csv, 1)
