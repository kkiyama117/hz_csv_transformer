use pyo3::prelude::*;
use pyo3::types::{PyDict, PyTuple};

#[pymodule(name = "csv_structure")]
pub fn module(m: &Bound<'_,PyModule>) -> PyResult<()> {
    m.add_class::<CSVInfo>()?;
    Ok(())
}

#[pyclass(subclass)]
struct CSVInfo {}

#[pymethods]
impl CSVInfo {
    #[new]
    #[pyo3(signature = (*py_args, **py_kwargs))]
    pub fn __new__(py_args: &PyTuple,py_kwargs: Option<&PyDict>) -> Self {
        CSVInfo {}
    }
}