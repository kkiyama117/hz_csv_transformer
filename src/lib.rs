use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::wrap_pymodule;

#[cfg(feature = "build_info")]
#[macro_use]
extern crate pyo3_built;

#[cfg(feature = "build_info")]
#[allow(dead_code)]
mod build {
    include!(concat!(env!("OUT_DIR"), "/built.rs"));
}

mod submodule;


#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
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


fn register_child_module(_py: Python<'_>, parent_module: &PyModule) -> PyResult<()> {
    let child_module = PyModule::new(_py, "child_module")?;
    child_module.add_function(wrap_pyfunction!(sum_as_string,child_module)?)?;
    parent_module.add_submodule(child_module)?;
    Ok(())
}

#[pymodule]
fn hv_csv_transformer(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<ExampleClass>()?;
    m.add_function(wrap_pyfunction!(sum_as_string,m)?)?;
    m.add_wrapped(wrap_pymodule!(submodule::submodule))?;
    register_child_module(_py, m)?;

    // Inserting to sys.modules allows importing submodules nicely from Python
    // e.g. from maturin_starter.submodule import SubmoduleClass

    let sys = PyModule::import(_py, "sys")?;
    let sys_modules: &PyDict = sys.getattr("modules")?.downcast()?;
    sys_modules.set_item("hv_csv_transformer.submodule", m.getattr("submodule")?)?;
    // sys_modules.set_item("hv_csv_transformer.ExampleClass", m.getattr("ExampleClass")?)?;
    sys_modules.set_item("hv_csv_transformer.child_module", m.getattr("child_module")?)?;

    // Build info
    #[cfg(feature = "build_info")]
    m.add(
        "_build_info_",
        pyo3_built!(_py, build, "build", "time", "deps", "features", "host", "target", "git"),
    )?;

    Ok(())
}