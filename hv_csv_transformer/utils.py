from dataclasses import asdict
from chardet.universaldetector import UniversalDetector
import pickle

from hv_csv_transformer.my_polars import CVTransformer
from hv_csv_transformer.parser import NextIterator, is_real_data


def convert_to_utf(filename):
    _data = None
    with open(filename, 'rb') as f:
        detector = UniversalDetector()
        for line in f:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        result = detector.result.get("encoding")
    if result != "utf8":
        if result == "SHIFT_JIS":
            result = "CP932"
        with open(filename, encoding=result) as f:
            _data = f.read()
        with open(filename, "w", encoding="utf8") as f:
            f.write(_data)


def info_to_csv(info):
    data_dict = asdict(info)
    with open("../test.pickle", mode="wb") as f:
        pickle.dump(info, f)
    pickle_to_info("")


def pickle_to_info(name):
    with open("../test.pickle", mode="rb") as f:
        res = pickle.load(f)
    print(res)


# generate origin 2021 data from parsed_csv
# parsed_csv: NextIterator
# area: area of electrode
# number: optional. set number of data if needed.
def generate_origin_data(parsed_csv: NextIterator, area: float, number: int = -1):
    for (count, _data) in enumerate(filter(is_real_data, parsed_csv)):
        if number < 0:
            _trans = CVTransformer(_data)
            yield _trans.create_origin_input_with_density(area)
        else:
            if number == count:
                _trans = CVTransformer(_data)
                yield _trans.create_origin_input_with_density(area)
