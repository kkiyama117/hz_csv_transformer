use pyo3::prelude::*;
use pyo3::types::PyList;


// https://pyo3.rs/v0.20.0/module#python-submodules
#[pymodule]
#[pyo3(name = "models")]
pub fn module(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<RowData>()?;
    m.add_class::<BlockData>()?;
    Ok(())
}

#[pyclass]
#[derive(Clone)]
struct RowData {
    title: String,
    japanese: String,
    start: i32,
    count: i32,
}

impl ToPyObject for RowData {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

#[pymethods]
impl RowData {
    #[new]
    pub fn __new__(title: String, japanese: String, start: Option<i32>, count: Option<i32>) -> Self {
        let _start = match start {
            None => 2,
            Some(x) => x
        };
        let _count = match count {
            None => 1,
            Some(x) => x
        };
        RowData {
            title,
            japanese,
            start: _start,
            count: _count,
        }
    }
    #[getter]
    fn get_title(&self) -> PyResult<String> {
        Ok(self.title.clone())
    }
    #[setter]
    fn set_title(&mut self, value: String) -> PyResult<()> {
        self.title = value;
        Ok(())
    }
    #[getter(japanese)]
    fn get_japanese(&self) -> PyResult<String> {
        Ok(self.japanese.clone())
    }
    #[setter(japanese)]
    fn set_japanese(&mut self, value: String) -> PyResult<()> {
        self.japanese = value;
        Ok(())
    }

    #[getter]
    fn get_start(&self) -> PyResult<i32> {
        Ok(self.start)
    }
    #[setter]
    fn set_start(&mut self, value: i32) -> PyResult<()> {
        self.start = value;
        Ok(())
    }

    #[getter]
    fn get_count(&self) -> PyResult<i32> {
        Ok(self.count)
    }
    #[setter]
    fn set_count(&mut self, value: i32) -> PyResult<()> {
        self.count = value;
        Ok(())
    }
}

#[pyclass]
struct BlockData {
    title: String,
    rows: Vec<RowData>,
    start: i32,
}

#[pymethods]
impl BlockData {
    #[new]
    pub fn __new__(title: String, rows: &PyList, start: Option<i32>) -> PyResult<Self> {
        let _start = match start {
            None => 1,
            Some(x) => x
        };
        let _rows = rows.extract::<Vec<RowData>>()?;
        Ok(BlockData {
            title,
            rows: _rows,
            start: _start,
        })
    }
    #[getter]
    fn get_title(&self) -> PyResult<String> {
        Ok(self.title.clone())
    }
    #[setter]
    fn set_title(&mut self, value: String) -> PyResult<()> {
        self.title = value;
        Ok(())
    }
    #[getter]
    fn get_start(&self) -> PyResult<i32> {
        Ok(self.start)
    }
    #[setter]
    fn set_start(&mut self, value: i32) -> PyResult<()> {
        self.start = value;
        Ok(())
    }

    #[getter]
    fn get_rows<'p>(&self, py: Python<'p>) -> PyResult<&'p PyList> {
        Ok(PyList::new(py, &self.rows))
    }
    #[setter]
    fn set_rows(&mut self, value: &PyList) -> PyResult<()> {
        self.rows = value.extract::<Vec<RowData>>()?;
        Ok(())
    }
}

