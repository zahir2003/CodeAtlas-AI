import logging
import sys

from app.core.config import LOGS_DIR

LOGS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_FILE = LOGS_DIR / "codeatlas.log"


def setup_logging():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                LOG_FILE,
                encoding="utf-8",
            ),
        ],
        force=True,
    )