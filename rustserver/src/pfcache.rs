/// pfcache "Persistent Functional Cache"

use std::collections::HashMap;
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use serde::{Serialize, Deserialize};

//#[derive(Serialize, Deserialize)]
pub struct PHash {
    hash: u64,
}

impl PHash {
    pub fn new<T: Hash>(t: &T) -> Self {
        let mut s = DefaultHasher::new();
        t.hash(&mut s);
        Self { hash: s.finish() }
    }
}

pub struct Cache {
    filename: String,
    map: HashMap<u64, String>,
}

/// This is all the possible errors that can happen with pfcaching
pub enum Error {
    PickleDB
}

impl Cache {
    pub fn new() -> Self {
        let embedding_cache_filename = std::env::var("EMBEDDING_CACHE")
            .unwrap_or("embedding_cache.db".to_string());
        Self {
            filename: embedding_cache_filename,
            map: HashMap::new(),
        }
    }
    pub fn dump(&mut self) -> Result<(), Error> {
        Ok(())
    }
    pub fn get<'a, K: Hash, V: Serialize>(key: &K, f: &dyn Fn(&K) -> &'a V) -> &'a V {
        f(key)
    }
}
