# Semi-auto CV-graph generator for HZ7000

## structure

### parser

`parser` parses output of HZ7000 CV measurement with dataclass structure.
it uses `polars` (similar with `pandas` but much faster!)

### my_polars

`my_polars` fix and add some data in parsed data.

### plotter

`plotter` makes CV-graph.

### Customize

#### Get data only for `origin2021`

edit and run `generate_origin_data`. see `main.py` also.

#### customize graph

edit `plotter`. `plotter` is based on `matplotlib`(and `seaborn`). 
