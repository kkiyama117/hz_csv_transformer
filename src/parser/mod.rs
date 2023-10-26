use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::wrap_pymodule;

mod models;

#[pymodule]
pub fn parser(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    // let sys_modules: &PyDict = PyModule::import(_py, "sys")?.getattr("modules")?.downcast()?;
    //
    // m.add_wrapped(wrap_pymodule!(models::module))?;
    // m.add_submodule();
    Ok(())
}
