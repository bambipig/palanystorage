from palanystorage.engine.base import Dialect
import oss2


class PalAliossDialect(Dialect):
    driver = 'pal_alioss'

    def __init__(self):
        super().__init__()

    def ready(self, *args, **kwargs):
        self.auth = oss2.Auth(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret)
        self.bucket = oss2.Bucket(
            auth=self.auth,
            endpoint=endpoint,
            bucket_name=self.bucket_name,
        )  # type: oss2.Bucket

