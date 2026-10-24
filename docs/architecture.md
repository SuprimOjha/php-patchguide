# Architecture

The CLI parses arguments; project inspection reads selected metadata; runtime detection calls php -v with a timeout; the advisory loader reads JSON; the evaluator compares numeric versions; report formatters output text or JSON.

Safety boundaries: no application code execution, no project file modifications, no network requests during local checks, and no project uploads. Vendor backports and production runtime differences require human verification.
