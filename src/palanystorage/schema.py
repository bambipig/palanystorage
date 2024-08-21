from dataclasses import dataclass
from dataclasses import field



@dataclass
class StorageConfigSchema:
    dialect: str
    driver: str
    root_path: str
    max_can_use: str
    bucket: str = field(default_factory=str)
    access_key: str = field(default_factory=str)
    access_key_secret: str = field(default_factory=str)
    inside_endpoint: str = field(default_factory=str)
    outside_endpoint: str = field(default_factory=str)
    region: str = field(default_factory=str)

    @property
    def storage_id(self) -> str:
        return f'{self.dialect}:{self.bucket}'


@dataclass
class WriteProgressSchema:
    storage_id: str
    key: str
    wrote_bytes: int
    total_bytes: int = None


@dataclass
class StoredObject:
    storage_id: str
    key: str
    url: str = None
    sha256_hash: str = None
