#!/usr/bin/env python3
"""No provider/model connection. Captures only synthetic fixture metadata."""
import json
import os
from pathlib import Path
import sys
if '--version' in sys.argv:
    print('codex-cli synthetic-1')
    sys.exit(0)
target = os.environ.get('FAKE_CODEX_CAPTURE')
if target:
    with open(target,'a') as f:
        f.write(json.dumps({'argv':sys.argv[1:],'cwd':os.getcwd(),
                            'role':os.environ.get('OAP_ROLE'),'home':os.environ.get('CODEX_HOME'),
                            'read_set':os.environ.get('OAP_INTENDED_READ_SET')})+'\n')
sys.exit(int(os.environ.get('FAKE_CODEX_EXIT','0')))
