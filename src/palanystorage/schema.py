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


@dataclass
class StoredObject:
    key: str
    url: str = None
