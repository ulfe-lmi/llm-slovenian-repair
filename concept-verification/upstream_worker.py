"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Owned
main-upstream resolver worker (child-side entry).

Order 022-a, requirement 4: this is the exact repository-local
versioned worker executed by the parent through the running
interpreter (``sys.executable`` with ``-I -S -B``) - no shell, no
pickling, no arbitrary executable, no endpoint search, no model or
agent.  The child owns the single potentially noninterruptible
phase the parent's timer cannot contain: the actual
``getaddrinfo`` resolution of one bounded host (an IP-literal host
never reaches the child).  It reads exactly one strict versioned
request frame from its private stdin pipe, performs at most one
resolution attempt (no automatic retry), and writes exactly one
strict versioned response frame to its private stdout pipe.  Its
environment is empty and its argv carries no body, request,
credential or secret data.  The child never logs: its stderr is
silenced and its stdout carries only the frame, so no raw exception
text, host or address can leak.  The authoritative setup deadline is
enforced by the parent, which terminates and reaps this child on
expiry.  Exit status: 0 after writing a well-formed frame
(including a transport-failure frame), nonzero only on a child-side
contract violation, which the parent rejects.
"""

from __future__ import annotations

import os
import sys

# Isolated mode (-I) does not prepend the script directory; insert
# this worker's own repository-local directory - the exact
# trusted versioned path the parent selected, not a search - before
# importing the paired protocol module.
_WORKER_DIR = os.path.dirname(os.path.abspath(__file__))
if _WORKER_DIR not in sys.path:
    sys.path.insert(0, _WORKER_DIR)

from upstream_setup import worker_main  # noqa: E402

if __name__ == "__main__":
    try:
        _devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(_devnull, 2)
        os.close(_devnull)
    except OSError:
        pass
    try:
        exit_code = worker_main()
    except BaseException:
        exit_code = 3
    sys.exit(exit_code)
