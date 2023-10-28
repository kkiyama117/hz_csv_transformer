use pyo3::prelude::*;
use pyo3::wrap_pymodule;
use pyo3::types::PyDict;

#[cfg(feature = "build_info")]
#[macro_use]
extern crate pyo3_built;

#[cfg(feature = "build_info")]
#[allow(dead_code)]
mod build {
    include!(concat!(env!("OUT_DIR"), "/built.rs"));
}

mod submodule;
mod parser;


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
    let sys_modules: &PyDict = PyModule::import(_py, "sys")?.getattr("modules")?.downcast()?;

    m.add_class::<ExampleClass>()?;
    sys_modules.set_item("hv_csv_transformer.ExampleClass", m.getattr("ExampleClass")?)?;

    m.add_function(wrap_pyfunction!(sum_as_string,m)?)?;

    m.add_wrapped(wrap_pymodule!(submodule::submodule))?;
    sys_modules.set_item("hv_csv_transformer.submodule", m.getattr("submodule")?)?;


    m.add_wrapped(wrap_pymodule!(parser::parser))?;
    // sys_modules.set_item("hv_csv_transformer.parser.models", m.getattr("parser")?)?;
    sys_modules.set_item("hv_csv_transformer.parser_rs", m.getattr("parser_rs")?)?;

    register_child_module(_py, m)?;
    sys_modules.set_item("hv_csv_transformer.child_module", m.getattr("child_module")?)?;
    // Inserting to sys.modules allows importing submodules nicely from Python
    // e.g. from maturin_starter.submodule import SubmoduleClass


    // Build info
    #[cfg(feature = "build_info")]
    m.add(
        "_build_info_",
        pyo3_built!(_py, build, "build", "time", "deps", "features", "host", "target", "git"),
    )?;

    Ok(())
}