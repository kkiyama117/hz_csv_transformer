from polars import DataFrame

from hv_csv_transformer.models.csv_structure import CVData
import polars as pl


def _refactor_cv_columns(df):
    _cols = df.columns
    df = df.drop("NoData0")
    df = df.drop("NoData1")
    df = df.with_columns(
        [
            df.drop_in_place("1 時間t").cast(pl.Float64).alias("time"),
            df.drop_in_place("2 電位E").cast(pl.Float64).alias("potential"),
            df.drop_in_place("3 電流I").cast(pl.Float64).alias("current"),
            df.drop_in_place("4 WE/CE").cast(pl.Float64).alias("working"),
            df.drop_in_place("種別").cast(str).alias("kind"),
        ]
    )
    return df


class CVTransformer:
    def __init__(self, data):
        if type(data) == CVData:
            self._data = data
            self.data = _refactor_cv_columns(data.data)
        else:
            # TODO: raise Error
            pass

    def calc(self, area):
        return self.calc_density(area)

    def calc_density(self, area: float) -> DataFrame:
        _nc = pl.col("current") * 1000 / area
        self.data = self.data.with_columns(_nc.alias("current density"))
        return self.data

    def create_origin_input_with_density(self, area: float) -> DataFrame:
        _data = self.calc_density(area)
        _data = _data.select("potential", "current density")
        return _data
