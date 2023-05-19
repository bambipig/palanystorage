from dataclasses import dataclass
from dataclasses import field
from palanystorage.const import DialectNames


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
        if self.dialect in [DialectNames.alioss.name]:
            return f'{self.dialect}:{self.bucket}'
        else:
            return ''


@dataclass
class StoredObject:
    storage_id: str
    key: str
    url: str = None

