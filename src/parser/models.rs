use pyo3::prelude::*;

#[pyclass]
struct RowData2{

}

// #[pymethods]
// impl SubmoduleClass {
//     #[new]
//     pub fn __new__() -> Self {
//         SubmoduleClass {}
//     }
//
//     pub fn greeting(&self) -> &'static str {
//         "Hello, world!"
//     }
// }

// https://pyo3.rs/v0.20.0/module#python-submodules
#[pymodule]
#[pyo3(name="models")]
pub fn module(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<RowData2>()?;
    Ok(())
}
