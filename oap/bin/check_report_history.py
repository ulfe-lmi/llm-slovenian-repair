#!/usr/bin/env python3
"""Read-only history-aware report immutability check."""
import sys

from oap_cli import main


if __name__ == "__main__":
    sys.exit(main(["report-history", *sys.argv[1:]]))
