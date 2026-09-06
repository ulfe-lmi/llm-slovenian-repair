#!/usr/bin/env python3
"""OAP state entry point; shared implementation and --help."""
import sys
from oap_cli import main
if __name__ == "__main__":
    sys.exit(main(["state", *sys.argv[1:]]))
