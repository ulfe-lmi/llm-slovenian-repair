#!/usr/bin/env python3
"""OAP publish entry point; shared implementation and --help."""
import sys
from oap_cli import main
if __name__ == "__main__":
    sys.exit(main(["publish", *sys.argv[1:]]))
