use pyo3::prelude::*;
use std::vec::Vec;

fn main() -> PyResult<()> {
    let py_embedder = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/embedder.py"));
    Python::with_gil(|py| {
        PyModule::from_code(py, py_embedder, "embedder", "embedder")?;
        let embedder_module = py.import("embedder")?;
        let embedder_class: Py<PyAny> = embedder_module.getattr("Embedder")?.into();
        let embedder: Py<PyAny> = embedder_class.call1(py, ("intfloat/e5-base-v2", ))?.into();

        println!("Object: {}", embedder);
        let res = embedder
            .call_method1(py, "embed", ([
                "What is your eye color?",
                "What is your favorite classic Hollywood flick?",
                "Is 8 a perfect number?",
                "Do you like painting?",
            ], "query: "))?
            .call_method0(py, "cpu")?
            .call_method0(py, "detach")?
            .call_method0(py, "numpy")?
            .call_method0(py, "tolist")?;
        let res2: Vec<Vec<f64>> = res.extract(py)?;
        println!("Results: {:#?}", res2);
        Ok(())
    })
}
