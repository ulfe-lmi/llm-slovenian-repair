#!/usr/bin/env python3
"""Read-only transcript coherence entry point; see --help for modes."""
import sys

from oap_cli import main


if __name__ == "__main__":
    sys.exit(main(["transcript", *sys.argv[1:]]))
