from dataclasses import asdict

import csv
from chardet.universaldetector import UniversalDetector
import pickle


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
    with open("test.pickle", mode="wb") as f:
        pickle.dump(info, f)
    pickle_to_info("")


def pickle_to_info(name):
    with open("test.pickle", mode="rb") as f:
        res = pickle.load(f)
    print(res)
