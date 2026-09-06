# Testing contract

TEST-01. Bootstrap infrastructure: `python3 -B -m unittest discover -s oap/tests -v`.
Use standard-library disposable Git/FIFO fixtures and fake CLI/GitHub boundaries.
No real model, corpus, customer data or protected service required. Tests must
exercise the real helper entry point/boundary and assert specific failure reasons.

TEST-02. Product is PLANNED. Future order names focused/broader test commands,
negative cases, tested SHA and real boundary. Never substitute a mock of the
boundary being claimed. PASS/FAIL/SKIPPED/NOT RUN/BLOCKED/PENDING/MISSING stay
distinct. Required skipped tests never pass. First reproducible failure determines
the smallest discriminating diagnostic experiment and its stop condition.

TEST-03. Separate fake-client correctness, installed CLI discovery, actual model
compatibility, human-labelled linguistic benefit, ICA and deployment authorization.
Live tests require explicit opt-in and verified endpoints/budgets/data rights.
Never weaken checks or call live Qwen to make scaffold tests pass. Detailed future
evaluation rationale is optional background in [evaluation](docs/EVALUATION.md).
