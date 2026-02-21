"""Enable `python -m crc_reverse`."""

import sys

from .cli import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
