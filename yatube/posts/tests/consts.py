import tempfile

from django.conf import settings

POSTS_FOR_TEST: int = 123
SHIFT: int = 1
ZERO: int = 0
DELAY: float = 0.01
MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
