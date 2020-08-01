import logging
import sys

logger = logging.getLogger()
logging.basicConfig(
    format="%(asctime)s: %(levelname)s:    %(message)s",
    level=getattr(logging, "DEBUG"),
    stream=sys.stdout
)
