import csv
from chardet.universaldetector import UniversalDetector


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
