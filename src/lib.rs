use pyo3::prelude::*;
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
mod parser;
mod models;


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


fn register_child_module(parent_module: &Bound<'_, PyModule>) -> PyResult<()> {
    let child_module = PyModule::new(parent_module.py(), "child_module")?;
    child_module.add_function(wrap_pyfunction!(sum_as_string,&child_module)?)?;
    parent_module.add_submodule(&child_module)?;
    Ok(())
}

#[pymodule]
fn hv_csv_transformer(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<ExampleClass>()?;
    // sys_modules.set_item("hv_csv_transformer.ExampleClass", m.getattr("ExampleClass")?)?;

    m.add_function(wrap_pyfunction!(sum_as_string,m)?)?;

    m.add_wrapped(wrap_pymodule!(submodule::submodule))?;
    // sys_modules.set_item("hv_csv_transformer.submodule", m.getattr("submodule")?)?;


    m.add_wrapped(wrap_pymodule!(parser::parser))?;
    // sys_modules.set_item("hv_csv_transformer.parser.models", m.getattr("parser")?)?;
    // sys_modules.set_item("hv_csv_transformer.parser_rs", m.getattr("parser_rs")?)?;
    m.add_wrapped(wrap_pymodule!(models::module))?;
    // sys_modules.set_item("hv_csv_transformer.models_rs", m.getattr("models_rs")?)?;

    register_child_module(m)?;
    // sys_modules.set_item("hv_csv_transformer.child_module", m.getattr("child_module")?)?;
    // Inserting to sys.modules allows importing submodules nicely from Python
    // e.g. from maturin_starter.submodule import SubmoduleClass


    // Build info
    let _py = m.py();
    #[cfg(feature = "build_info")]
    m.add(
        "_build_info_",
        pyo3_built!(_py, build, "build", "time", "deps", "features", "host", "target", "git"),
    )?;

    Ok(())
}