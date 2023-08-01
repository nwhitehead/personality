/// pfcache "Persistent Functional Cache"
// A pfcache is file backed, everything is serialized to the file when dumped

use std::collections::HashMap;
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use std::marker::PhantomData;
use serde::{Serialize, Deserialize};
use serde::de::DeserializeOwned;
use std::io::Write;
use std::fs::File;
use postcard::{from_bytes, to_stdvec};

pub fn compute_hash<T: Hash>(t: &T) -> u64 {
    let mut s = DefaultHasher::new();
    t.hash(&mut s);
    s.finish()
}

pub struct Cache<K, V>
{
    filename: String,
    map: HashMap<u64, String>,
    _marker: std::marker::PhantomData<(K, V)>,
}

/// This is all the possible errors that can happen with pfcaching
#[derive(Debug)]
pub enum Error {
    NotFound,
    Serialize(serde_json::Error),
    PostcardSerialize(postcard::Error),
    IOError(std::io::Error),
}

impl From<serde_json::Error> for Error {
    fn from(err: serde_json::Error) -> Self {
        Error::Serialize(err)
    }
}

impl From<postcard::Error> for Error {
    fn from(err: postcard::Error) -> Self {
        Error::PostcardSerialize(err)
    }
}

impl From<std::io::Error> for Error {
    fn from(err: std::io::Error) -> Self {
        Error::IOError(err)
    }
}

impl <K, V> Cache<K, V> where
    K: Hash,
    V: Serialize,
    V: DeserializeOwned,
{
    pub fn new() -> Self {
        let embedding_cache_filename = std::env::var("EMBEDDING_CACHE")
            .unwrap_or("embedding_cache.db".to_string());
        Self {
            filename: embedding_cache_filename,
            map: HashMap::new(),
            _marker: PhantomData,
        }
    }
    pub fn dump(&mut self) -> Result<(), Error> {
        let mut file = File::create(&self.filename)?;
        let vec = postcard::to_stdvec(&self.map)?;
        file.write_all(&vec)?;
        Ok(())
    }
    pub fn has(&self, key: K) -> bool {
        let h = compute_hash(&key);
        self.map.get(&h).is_some()
    }
    pub fn get(&self, key: K) -> Result<V, Error>
    {
        let h = compute_hash(&key);
        match self.map.get(&h) {
            Some(value) => Ok(serde_json::from_str(&value)?),
            _ => Err(Error::NotFound)
        }
    }
    pub fn set(&mut self, key: K, value: V) -> Result<(), Error>
    {
        let h = compute_hash(&key);
        let vs = serde_json::to_string(&value)?;
        self.map.insert(h, vs);
        Ok(())
    }
}
