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
    # sns.set_theme()
    plt.rcParams["font.family"] = "Meiryo"
    _meta = GraphInfo(
        x_title="potential",
        y_title="current density",
        hue="凡例")
    fig, axes = plt.subplots()
    # fig.suptitle("CV graph")
    bars = (x for x in parsed_csv if is_real_data(x))
    for (count, data) in enumerate(bars):
        _trans = CVTransformer(data)
        _trans.calc(area)
        # print(_trans.data.glimpse())
        # print(_trans.data)
        axes.plot(_trans.data[_meta.x_title], _trans.data[_meta.y_title], label=f"{count}回目")
    axes.legend()
    axes.set_ylabel(r"$Current\ Density\ (mA\ cm^{-2}$)")
    axes.set_xlabel("Potential v.s. Al/Al(III) (V)")

    plt.savefig('sample.png')
    plt.show()
    # matplotlib.pyplot.show(block=False)
