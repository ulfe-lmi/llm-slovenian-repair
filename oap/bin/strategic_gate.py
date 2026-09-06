#!/usr/bin/env python3
"""OAP strategic-gate entry point; shared implementation and --help."""
import sys
from oap_cli import main
if __name__ == "__main__":
    sys.exit(main(["strategic-gate", *sys.argv[1:]]))
