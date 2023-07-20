/// pfcache "Persistent Functional Cache"

use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use pickledb::{PickleDb, PickleDbDumpPolicy, SerializationMethod};

pub fn func(name: &str) {
    println!("Hello {}", name.to_string());
}

pub fn calculate_hash<T: Hash>(t: &T) -> u64 {
    let mut s = DefaultHasher::new();
    t.hash(&mut s);
    s.finish()
}

pub struct Cache {
    db: PickleDb,
}

pub enum Error {
    PickleDB
}

impl Cache {
    pub fn new() -> Self {
        let embedding_cache_filename = std::env::var("EMBEDDING_CACHE")
            .unwrap_or("embedding_cache.db".to_string());
        Self { db: PickleDb::new(embedding_cache_filename, PickleDbDumpPolicy::DumpUponRequest, SerializationMethod::Json) }
    }
    pub fn dump(&mut self) -> Result<(), Error> {
        self.db.dump().map_err(|_| Error::PickleDB)
    }
}
