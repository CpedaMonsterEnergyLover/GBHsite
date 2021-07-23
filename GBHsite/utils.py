import mimetypes
from urllib.parse import urlparse


def calc_level(exp):
    return exp // 1000


def calc_left_exp(exp):
    return exp % 1000


def split_url(url):
    parse_object = urlparse(url)
    return parse_object.netloc, parse_object.path


VALID_IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png"
]


def valid_url_extension(url):
    return any([url.endswith(e) for e in VALID_IMAGE_EXTENSIONS])


VALID_IMAGE_MIMETYPES = [
    "image"
]


def valid_url_mimetype(url):
    mimetype, encoding = mimetypes.guess_type(url)
    if mimetype:
        return any([mimetype.startswith(m) for m in VALID_IMAGE_MIMETYPES])
    else:
        return False
