use pyo3::prelude::*;
use std::vec::Vec;
use pickledb::{PickleDb, PickleDbDumpPolicy, SerializationMethod};
use serde::{Deserialize, Serialize};
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

fn calculate_hash<T: Hash>(t: &T) -> u64 {
    let mut s = DefaultHasher::new();
    t.hash(&mut s);
    s.finish()
}

pub struct Embedder {
    pyobj: Py<PyAny>
}

impl Embedder {
    pub fn new() -> Self {
        let py_embedder = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/embedder.py"));
        Python::with_gil(|py| {
            PyModule::from_code(py, py_embedder, "embedder", "embedder")?;
            let embedder_module = py.import("embedder")?;
            let embedder_class: Py<PyAny> = embedder_module.getattr("Embedder")?.into();
            let embedder: Py<PyAny> = embedder_class.call1(py, ("intfloat/e5-base-v2", ))?.into();
            Ok::<Embedder, PyErr>(Self { pyobj: embedder })
        }).expect("Python did not return embedder")
    }
}

fn main() -> PyResult<()> {
    let embedding_cache_filename = std::env::var("EMBEDDING_CACHE")
    .expect("EMBEDDING_CACHE must be set to writable filename location");
    let mut db = PickleDb::new(embedding_cache_filename, PickleDbDumpPolicy::DumpUponRequest, SerializationMethod::Json);
    let py_embedder = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/embedder.py"));
    let data = vec![
        "What is your eye color?",
        "What is your favorite classic Hollywood flick?",
        "Is 8 a perfect number?",
        "Do you like painting?",
    ];
    Python::with_gil(|py| {
        PyModule::from_code(py, py_embedder, "embedder", "embedder")?;
        let embedder_module = py.import("embedder")?;
        let embedder_class: Py<PyAny> = embedder_module.getattr("Embedder")?.into();
        let embedder: Py<PyAny> = embedder_class.call1(py, ("intfloat/e5-base-v2", ))?.into();

        let res = embedder
            .call_method1(py, "embed", (data.clone(), "query: "))?
            .call_method0(py, "cpu")?
            .call_method0(py, "detach")?
            .call_method0(py, "numpy")?
            .call_method0(py, "tolist")?;
        let res2: Vec<Vec<f64>> = res.extract(py)?;
        for i in 1..res2.len() {
            let h = calculate_hash(&data[i]);
            println!("result {}: {} => {:#x} {:.3} {:.3} ... {:.3}", i, &data[i], h, res2[i][0], res2[i][1], res2[i][767]);
        }
        Ok(())
    })
}
