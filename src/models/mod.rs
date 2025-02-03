use pyo3::prelude::*;
use pyo3::wrap_pymodule;

mod csv_structure;

#[pymodule(name = "models_rs")]
pub(super) fn module(m: &Bound<'_,PyModule>) -> PyResult<()> {
    m.add_wrapped(wrap_pymodule!(csv_structure::module))?;
    // let sys_modules: &PyDict = PyModule::import(_py, "sys")?.getattr("modules")?.downcast()?;
    // sys_modules.set_item("hv_csv_transformer.models_rs.csv_structure", m.getattr("csv_structure")?)?;
    Ok(())
}
