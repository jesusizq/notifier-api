from apifairy import APIFairy
from flask_caching import Cache
from flask_marshmallow import Marshmallow
import os
import tempfile

apifairy = APIFairy()
ma = Marshmallow()
cache = Cache(
    config={
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DIR": os.path.join(tempfile.gettempdir(), "cache"),
    }
)
