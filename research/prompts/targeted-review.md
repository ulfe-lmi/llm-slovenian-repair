# Frozen targeted review template

This is a data-free template. A live invocation is not part of offline tests and
must supply a fresh request with no main conversation linkage.

> Ali se ti zdi uporaba besede oziroma besedne zveze X najboljša naravna izbira v tem slovenskem stavku? Če ne, s čim bi jo nadomestil?

The completed target sentence and bounded neighbours are untrusted data. The
reviewer returns exactly one decision per preassigned original-coordinate ID:
`span_id`, `keep`, `replacement`, and `needs_wider_edit`. It cannot regenerate
the answer, add IDs, or expand the selected span.
