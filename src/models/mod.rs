use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::wrap_pymodule;

mod csv_structure;

#[pymodule]
#[pyo3(name = "models_rs")]
pub fn module(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pymodule!(csv_structure::module))?;
    let sys_modules: &PyDict = PyModule::import(_py, "sys")?.getattr("modules")?.downcast()?;
    sys_modules.set_item("hv_csv_transformer.models_rs.csv_structure", m.getattr("csv_structure")?)?;
    Ok(())
}
