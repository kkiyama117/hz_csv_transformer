use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::wrap_pymodule;

mod models;

#[pymodule]
#[pyo3(name = "parser_rs")]
pub fn parser(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pymodule!(models::module))?;
    let sys_modules: &PyDict = PyModule::import(_py, "sys")?.getattr("modules")?.downcast()?;
    sys_modules.set_item("hv_csv_transformer.parser_rs.models", m.getattr("models")?)?;
    // m.add_submodule();
    Ok(())
}
