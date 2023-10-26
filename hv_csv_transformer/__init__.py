from hv_csv_transformer import *

# import the contents of the Rust library into the Python extension
# optional: include the documentation from the Rust module
from hv_csv_transformer.hv_csv_transformer import sum_as_string, ExampleClass, submodule, child_module, parser
try:
    from hv_csv_transformer.hv_csv_transformer import __all__ as all_rust, __doc__
except ImportError:
    all_rust = []
    print("RUST ERROR")

__all__ = all_rust + [
    # Python
    "models",
    "my_polars",
    "parser",
    "plotter",
    "utils",
    "PythonClass"
]


class PythonClass:
    def __init__(self, value: int) -> None:
        self.value = value
