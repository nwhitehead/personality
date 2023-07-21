/// pfcache "Persistent Functional Cache"
// A pfcache is file backed, everything is serialized to the file when dumped

use std::collections::HashMap;
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use serde::{Serialize, Deserialize};
use serde::de::DeserializeOwned;
use serde_json;

pub fn compute_hash<T: Hash>(t: &T) -> u64 {
    let mut s = DefaultHasher::new();
    t.hash(&mut s);
    s.finish()
}

pub struct Cache {
    filename: String,
    map: HashMap<u64, String>,
}

/// This is all the possible errors that can happen with pfcaching
pub enum Error {
    PickleDB
}

impl Cache where
{
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
    pub fn get<K, V> (&mut self, key: K, f: &dyn Fn(K) -> V) -> V 
    where
        K: Hash,
        V: DeserializeOwned,
        V: Serialize,
    {
        let h = compute_hash(&key);
        let existing = self.map.get(&h);
        match existing {
            Some(value) => serde_json::from_str(&value).unwrap(),
            None => {
                let value = f(key);
                let svalue = serde_json::to_string(&value).unwrap();
                self.map.insert(h, svalue.clone());
                value
            }
        }
    }
}
