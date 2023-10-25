use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::wrap_pymodule;


#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pymodule]
fn hv_csv_transformer(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<ExampleClass>()?;
    // m.add_wrapped(wrap_pymodule!())
    m.add_function(wrap_pyfunction!(sum_as_string,m)?)?;

    // Inserting to sys.modules allows importing submodules nicely from Python
    // e.g. from maturin_starter.submodule import SubmoduleClass

    let sys = PyModule::import(_py, "sys")?;
    let sys_modules: &PyDict = sys.getattr("modules")?.downcast()?;
    // sys_modules.set_item("hv_csv_transformer.submodule", m.getattr("submodule")?)?;

    Ok(())
}

#[pyclass]
struct ExampleClass {
    #[pyo3(get, set)]
    value: i32,
}

#[pymethods]
impl ExampleClass {
    #[new]
    pub fn new(value: i32) -> Self {
        ExampleClass { value }
    }
}

