#!/usr/bin/env python3
"""Read-only fake gh protocol driven by explicit synthetic JSON responses."""
import json
import os
import sys
from pathlib import Path
assert sys.argv[1]=='api', 'fake accepts read-only api only'
data = json.loads(Path(os.environ['FAKE_GH_RESPONSES']).read_text())
key = sys.argv[2]
if key not in data:
    sys.exit(3)
print(json.dumps(data[key]))
