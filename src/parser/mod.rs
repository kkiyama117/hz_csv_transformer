use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::wrap_pymodule;

mod models;

#[pymodule(name = "parser_rs")]
pub fn parser(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pymodule!(models::module))?;
    // m.add_submodule();
    Ok(())
}
