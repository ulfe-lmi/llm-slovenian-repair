#!/usr/bin/env python3
"""OAP governance entry point; shared implementation and --help."""
import sys
from oap_cli import main
if __name__ == "__main__":
    sys.exit(main(["governance", *sys.argv[1:]]))
