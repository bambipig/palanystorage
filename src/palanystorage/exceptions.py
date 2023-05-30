from enum import Enum


class BaseException(Exception):
    class Eid(Enum):
        pass

    def __init__(self, eid: Eid, **kwargs):
        self.eid = eid


class UnknownDialect(BaseException):
    pass


class UnknownDriver(BaseException):
    pass


class WriteFileFailed(BaseException):
    class Eid(Enum):
        storage_upload_failed = 'storage upload failed'


class DeleteFileFailed(BaseException):
    class Eid(Enum):
        storage_delete_failed = 'storage delete failed'
