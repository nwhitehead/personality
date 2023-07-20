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

#[derive(PartialEq)]
pub enum TextType {
    Passage,
    Query,
}

fn text_of_texttype(t:TextType) -> &str {
    match t {
        
    }
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
    pub fn embed(&self, texts:Vec<&str>, textType:TextType) -> Vec<Vec<f32>> {
        Python::with_gil(|py| {
            Ok::<Vec<Vec<f32>>, PyErr>(self.pyobj
                .call_method1(py, "embed", (texts.clone(), if textType == TextType::Query { "query: " } else { "passage: " }))?
                .call_method0(py, "cpu")?
                .call_method0(py, "detach")?
                .call_method0(py, "numpy")?
                .call_method0(py, "tolist")?
                .extract(py)?)
        }).expect("Python did not return embedding")
    }
}

fn main() -> () {
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
    let emb = Embedder::new();
    let res = emb.embed(data.clone(), TextType::Query);
    for i in 1..res.len() {
        let h = calculate_hash(&data[i]);
        println!("result {}: {} => {:#x} {:.3} {:.3} ... {:.3}", i, &data[i], h, res[i][0], res[i][1], res[i][767]);
    }
}
