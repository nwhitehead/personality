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
#[derive(Debug)]
pub enum Error {
    NotFound,
    Serialize(serde_json::Error),
}

impl From<serde_json::Error> for Error {
    fn from(err: serde_json::Error) -> Self {
        Error::Serialize(err)
    }
}

impl Cache
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
    pub fn has<K: Hash> (&self, key: K) -> bool {
        let h = compute_hash(&key);
        self.map.get(&h).is_some()
    }
    pub fn get<K, V> (&self, key: K) -> Result<V, Error>
    where
        K: Hash,
        V: DeserializeOwned,
    {
        let h = compute_hash(&key);
        match self.map.get(&h) {
            Some(value) => Ok(serde_json::from_str(&value)?),
            _ => Err(Error::NotFound)
        }
    }
    pub fn set<K, V> (&mut self, key: K, value: V) -> Result<(), Error>
    where
        K: Hash,
        V: Serialize,
    {
        let h = compute_hash(&key);
        let vs = serde_json::to_string(&value)?;
        self.map.insert(h, vs);
        Ok(())
    }
}
