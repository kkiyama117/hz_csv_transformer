import dataclasses

import matplotlib.pyplot as plt

from my_polars import CVTransformer
from parser import is_real_data, NextIterator
import seaborn as sns


@dataclasses.dataclass
class GraphInfo:
    x_title: str
    y_title: str
    hue: str
    kind: str = "line"


def create_cv_graph_all(parsed_csv: NextIterator, area: float):
    sns.set_theme()
    _meta = GraphInfo(
        x_title="potential",
        y_title="current density",
        hue="凡例")
    fig, axes = plt.subplots()
    fig.suptitle("CV graph")
    for data in parsed_csv:
        if is_real_data(data):
            _trans = CVTransformer(data)
            _trans.calc(area)
            print(_trans.data.glimpse())
            print(_trans.data)
            axes.plot(_trans.data[_meta.x_title], _trans.data[_meta.y_title])
    axes.set_ylabel("Current Density (mA cm-2)")
    axes.set_xlabel("Potential v.s. Al/Al(III) (V)")

    axes.legend()
    plt.savefig('sample.png')
    plt.show()
    # matplotlib.pyplot.show(block=False)
